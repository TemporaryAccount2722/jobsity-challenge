# Jobsity Challenge

This repository provides an implementation for a challenge provided by Jobsity

The challenge was to develop an on-demand pipeline for ingesting data into a SQL database. The data represents trips taken by different vehicles, and include a city, a point of origin and a destination.

I've developed a REST API to receive and store the data on a PostgreSQL database on-demand.

## REST API
The REST API consist of 3 routes: one to send data to be stored, and two to get some specifc information from the database (weekly average number of trips for an area, defined either by a bounding given by coordinates or by a region), as requested


#### POST /trips
Receives a JSON array containing the data to be stored.

Example:
```bash
curl --request POST \
  --url https://djc2qulcbe.execute-api.us-east-1.amazonaws.com/v1/trips \
  --header 'Content-Type: application/json' \
  --data '{
	"records": [
		{
			"region": "Prague",
			"origin_coord": "POINT (14.4973794438195 50.00136875782316)",
			"destination_coord": "POINT (14.43109483523328 50.04052930943246)",
			"datetime": "2018-05-28 9:03:40",
			"datasource": "funny_car"
		},
		{
			"region": "Turin",
			"origin_coord": "POINT (7.672837913286881 44.9957109242058)",
			"destination_coord": "POINT (7.720368637535126 45.06782385393849)",
			"datetime": "2018-05-21 2:54:04",
			"datasource": "baba_car"
		}
	]
}'
```



#### GET /trips_by/coordinates

Returns the weekly average trips for the area between the two points.

Query parameters:

| Parameter | Explanation               |
|-----------|---------------------------|
| latx      | First bounding latitude   |
| laty      | Second bounding latitute  |  
| lonx      | First bounding longitude  |  
| lony      | Second bounding longitude | 

Example:
```bash
curl --request GET \
  --url 'https://djc2qulcbe.execute-api.us-east-1.amazonaws.com/v1/trips_by/coordinates?latx=13.001&laty=15.564&lonx=50&lony=52'
```


#### GET /trips_by/region

Returns the weekly average trips for the region.

Query parameters:

| Parameter   | Explanation                   |
|-------------|-------------------------------|
| region      | Name of the region to fetch   |

Example:
```bash
curl --request GET \
  --url 'https://djc2qulcbe.execute-api.us-east-1.amazonaws.com/v1/trips_by/region?region=Prague' \
```