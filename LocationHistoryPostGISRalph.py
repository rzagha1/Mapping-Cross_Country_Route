def Google_CrossCounty_Route(jsonfile):
    #Parses Google Maps Location History JSON file into a points table in PostgreSQL
    #Intersects the google points with a US state shapefile/table
    #Creates a linestring table displaying routes by state and date stamp
    import psycopg2
    import os
    import sys
    import json
    from datetime import datetime
    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='mypass' port = '5432' ") #connecting to DB
    cur = conn.cursor()  #setting up connection cursor
    cur.execute('''drop table ccpoints''')
    #setting up route points table
    cur.execute('''CREATE TABLE ccpoints
                (pid serial primary key,
                 lat float,
                 long float,
                 datereal text,
                 datetosort text,
                 routes geometry);''')
    lat = ""
    longitude = ""
    datesort = ""
    datereal = ""
    activity = ""
    j = json.load(open(jsonfile))
    for loc,att in j.items():
        for line in att:
            for y,z in line.items():
                if y == "latitudeE7": lat = z * 0.0000001
                elif y == "longitudeE7": longitude = z * 0.0000001
                elif y == "timestampMs":
                    datesort = str(datetime.fromtimestamp(int(z)/1000))[0:10]
                    datereal = str(datetime.fromtimestamp(int(z)/1000))
            cur.execute(""" insert into ccpoints (lat, long, datereal,datetosort, routes)
            values(%s,%s,%s,%s,ST_SetSRID(ST_MakePoint(%s, %s), 4269))""",(lat,longitude,datereal,datesort,longitude,lat))
    cur.execute("""drop table RoutePostGIS""")
    cur.execute("""CREATE TABLE RoutePostGIS as
    SELECT s.name as state, r.datetosort as date, ST_MakeLine(r.routes ORDER BY r.datereal) as geom
        FROM ccpoints AS r INNER JOIN states as s ON st_intersects(s.geom,r.routes)
            GROUP BY s.name, r.datetosort ORDER BY r.datetosort;""")
    conn.commit()

jfile = r'path\LocationHistory.json'
Google_CrossCounty_Route(jfile)