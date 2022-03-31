import json
import psycopg2
from psycopg2.extras import RealDictCursor
import re
import os

DATABASE_HOST = os.environ['DATABASE_HOST']
DATABASE_NAME = os.environ['DATABASE_NAME']
DATABASE_USER = os.environ['DATABASE_USER']
DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']
DATABASE_PORT = os.environ['DATABASE_PORT']

def lambda_handler(event, context):
    latx = float(event['queryStringParameters']['latx'])
    laty = float(event['queryStringParameters']['laty'])
    lonx = float(event['queryStringParameters']['lonx'])
    lony = float(event['queryStringParameters']['lony'])
    
    conn = psycopg2.connect(host=DATABASE_HOST, database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, port=DATABASE_PORT)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    query =  f"""
    SELECT 
        date_trunc('week', datetime) AS week,
        count(1) AS trips
    FROM 
        trips 
    WHERE
        ((origin_coord_lat > {latx} AND origin_coord_lat < {laty} OR
        origin_coord_lat < {latx} AND origin_coord_lat > {laty}) AND
        (origin_coord_long > {lonx} AND origin_coord_long < {lony} OR
        origin_coord_long < {lonx} AND origin_coord_long > {lony}))
        OR
        ((destination_coord_lat > {latx} AND destination_coord_lat < {laty} OR
        destination_coord_lat < {latx} AND destination_coord_lat > {laty}) AND
        (destination_coord_long > {lonx} AND destination_coord_long < {lony} OR
        destination_coord_long < {lonx} AND destination_coord_long > {lony}))
    GROUP BY 1;
    """.format(latx, laty, lonx, lony)
    
    cursor.execute(query)
    
    results = cursor.fetchall()
    
    return {
        'statusCode': 200,
        'body': json.dumps(results, default=str)
    }
