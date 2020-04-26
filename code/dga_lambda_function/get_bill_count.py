import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from helper import updateKey
"""
   For this version, I consider the calling times of both billing and apikeys endpoints in 'counts',
   When customer sends requests, first I will check if their apikey already existed in database, if
   already exists, update the record.
   query_key can be different from api_key since a user can have two keys.
"""
def lambda_handler(event, context):
    query_key = event['headers']['x-api-key']
    api_key = event['queryStringParameters']['api_key']
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    table = dynamodb.Table('apikey_counts')
    updateKey(query_key, table)
    ### get counts for api_key
    new_response = table.get_item(
        Key={
            'api_key':api_key
        }
    )
    call_frequency = new_response['Item']['apikey_counts']
    event['api_key'] = api_key
    event['apikey_counts'] = str(call_frequency)
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }









