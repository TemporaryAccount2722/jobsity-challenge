import json
import psycopg2
import re
import os

DATABASE_HOST = os.environ['DATABASE_HOST']
DATABASE_NAME = os.environ['DATABASE_NAME']
DATABASE_USER = os.environ['DATABASE_USER']
DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']
DATABASE_PORT = os.environ['DATABASE_PORT']

def insert_into_database(records):
    conn = psycopg2.connect(host=DATABASE_HOST, database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, port=DATABASE_PORT)
    cursor = conn.cursor()
    
    for record in records:
        query =  "INSERT INTO trips (region, origin_coord_lat, origin_coord_long, destination_coord_lat, destination_coord_long, datetime, datasource) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        data = (record['region'], record['origin_coord_lat'], record['origin_coord_long'], record['destination_coord_lat'], 
        record['destination_coord_long'], record['datetime'], record['datasource'])
        
        cursor.execute(query, data)
        
    conn.commit()
    
def format_record(record):
    origin_coord_lat = re.sub(r".*\(| \d.*", "", record['origin_coord'])
    origin_coord_long = re.sub(r".* |\)", "", record['origin_coord'])
    destination_coord_lat = re.sub(r".*\(| \d.*", "", record['destination_coord'])
    destination_coord_long = re.sub(r".* |\)", "", record['destination_coord'])
    
    return {
        "region": record['region'],
        "origin_coord_lat": origin_coord_lat,
        "origin_coord_long": origin_coord_long,
        "destination_coord_lat": destination_coord_lat,
        "destination_coord_long": destination_coord_long,
        "datetime": record['datetime'],
        "datasource": record['datasource']
    }
    
def lambda_handler(event, context):
    records = json.loads(event['body'])['records']
    
    records = list(map(format_record, records))
    insert_into_database(records)
    
    return {
        'statusCode': 200,
        'body': json.dumps("Records written")
    }