# Mapping_Cross_Country_Route

Using Python/PostGIS and Python/Fiona/Shapely to create routes from my google maps location data

1. Download Location History from google maps. https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=google%20maps%20timeline%20history *note location needs to be turned on and google maps needs to be the default mapping app (usually not the case for iphones). Click on settings, download a copy of your data, and download it as a zipped JSON file

2. Download the Country, state, or county shapefile for your analysis. For my routes I used this US states shapefile where the column 'name' is the state names (http://www2.census.gov/geo/tiger/GENZ2015/shp/cb_2015_us_state_500k.zip). *note if you use a different shapefile than mine you either have the change the shapefile name to 'states' and the column name containing the boundaries to 'name' or edit my script

3. Upload shapefile to PostgreSQL using the shapefile/DBF loader, ogr2ogr or python

4. Enter Google maps location history JSON file path to function

5. Export shapefile and convert to KML to view in google maps - *You can use QGIS, ArcGIS, Python/Fiona
