import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from helper import updateKey

"""
   Updating counts for query_key and then return all keys stored in database 
"""


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    table = dynamodb.Table('apikey_counts')
    query_key = event['headers']['x-api-key']
    updateKey(query_key, table)
    # get all api_keys stored in dynamodb
    resp = table.scan(AttributesToGet=['api_key'])
    all_keys = [i['api_key'] for i in resp['Items']]
    return {
        'statusCode': 200,
        'body': json.dumps(all_keys)
    }