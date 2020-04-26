import json
import logging
import boto3
from boto3.dynamodb.conditions import Key, Attr
from helper import updateKey
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    table = dynamodb.Table('apikey_counts')
    query_key = event['headers']['x-api-key']
    key = table.scan(FilterExpression=Attr('api_key').contains(query_key))['Items']
    updateKey(query_key, table)
    query_parms = event['queryStringParameters']
    domain_name = query_parms['fqdn']
    logger.info(msg=query_parms)
    if random.randint(0,10) % 2 == 0:
        query_parms['dga'] = False
    else:
        query_parms['dga'] = False
    logger.info(msg=query_parms)
    return {
        'statusCode': 200,
        'body': json.dumps(query_parms)
    }