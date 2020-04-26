import boto3
from boto3.dynamodb.conditions import Key, Attr

def updateKey(query_key, table):
    key = table.scan(FilterExpression=Attr('api_key').contains(query_key))['Items']
    ### update counts for query key
    if not key:
        table.put_item(
            Item={'api_key': query_key, 'apikey_counts': 1}
        )
    else:
        response = table.get_item(
            Key={
                'api_key': query_key
            }
        )
        count = response['Item']['apikey_counts'] + 1
        table.update_item(
            Key={
                'api_key': query_key
            },
            UpdateExpression='SET apikey_counts = :c',
            ExpressionAttributeValues={
                ':c': count
            }
        )