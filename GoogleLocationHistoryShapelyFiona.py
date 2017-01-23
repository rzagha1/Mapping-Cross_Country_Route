import os
import sys
import json
import fiona
from shapely.geometry import mapping,LineString,Point,shape
from shapely.wkt import loads,load
from fiona.crs import from_epsg
from datetime import datetime

def Google_Locations_Shapely(jsonfile,statefile,outputfile):
    lat = ""
    longitude = ""
    datesort = ""
    datereal = ""
    activity = ""
    x=json.load(open(jsonfile))
    with fiona.collection(statefile) as features:
        states = {f['properties']['NAME']: shape(f['geometry']) for f in features}
    crs = from_epsg(4269)
    schema = {'geometry': 'LineString', 'properties': {'State':'str','Date': 'str'}}
    coords = {}
    with fiona.open(outputfile, "w", "ESRI Shapefile", schema, crs) as output:
        for loc,att in x.items():
            for line in att:
                for y,z in line.items():
                    if y == "latitudeE7": lat = z * 0.0000001
                    elif y == "longitudeE7": longitude = z * 0.0000001
                    elif y == "timestampMs":
                        datesort = str(datetime.fromtimestamp(int(z)/1000))[0:10]
                        datereal = str(datetime.fromtimestamp(int(z)/1000))
                if datesort not in coords:
                    coords[datesort] = [(longitude,lat)]
                coords[datesort].append((longitude,lat))
        for k,v in sorted(coords.items()):
            ls = LineString(v)
            for k2,v2 in states.items():
                if ls.intersects(v2):
                    output.write({'properties':{'State':k2,'Date': k},
                    'geometry': mapping(ls)})
    return "Noury Chemtob"

jsonfile = r'\LocationHistory.json'
states = r"\MyRoutes\States.shp"
outfile = r"\RouteShapely.shp"
Google_Locations_Shapely(jsonfile,states,outfile)
