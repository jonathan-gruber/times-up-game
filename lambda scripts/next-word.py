import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import decimal


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def nextword(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('timesup-words')
    scoretable = dynamodb.Table('timesup-score')
    query_param = event['queryStringParameters']
    remove = query_param['remove']
    currentword = query_param['word']
    team=query_param['team']

    if (remove == 'yes'):
        responsescore = scoretable.update_item(
            Key={
                'team': team
                },
            UpdateExpression = 'SET score = score + :val',
            #ExpressionAttributeNames={
            #    '#score': 'score'
            #    },
            ExpressionAttributeValues = {
                ':val': decimal.Decimal(1)
                },
            ReturnValues='UPDATED_NEW'
        )
        print("INCREMENT UpdateItem succeeded:")

        
        response = table.update_item(
            Key={
                'word': currentword
            },
            UpdateExpression='SET #VALUE = :free',
            ExpressionAttributeNames={
                '#VALUE': 'free',
            },
            ExpressionAttributeValues={
                ':free': 'no'
            },
            ReturnValues='UPDATED_NEW'
        )
        

    response = table.scan(
        FilterExpression=Attr("free").eq('yes')
    )
    
    freewords = []
    for i in response['Items']:
        freewords.append(i)

    body_response = json.dumps(response, indent=4, cls=DecimalEncoder)

    return {
        "statusCode": 200,
        "body": body_response, 
                "headers": { 
            "Access-Control-Allow-Origin": "*" 
        }
            }