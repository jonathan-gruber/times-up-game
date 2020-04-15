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

def clearwords(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('timesup-words')

    response = table.scan(
        FilterExpression=Attr("free").eq('no')
    )
    print(response)
    for wordz in response['Items']:
        print("wordzzzz")
        print(wordz["word"])
        response2 = table.update_item(
            Key={
                'word': wordz["word"]
            },
            UpdateExpression='SET #VALUE = :free',
            ExpressionAttributeNames={
                '#VALUE': 'free',
            },
            ExpressionAttributeValues={
                ':free': 'yes'
            },
            ReturnValues='UPDATED_NEW'
        )
        

    response3 = table.scan(
        FilterExpression=Attr("free").eq('yes')
    )
    body_response = json.dumps(response3, indent=4, cls=DecimalEncoder)

    return {
        "statusCode": 200,
        "body": body_response, 
                "headers": { 
            "Access-Control-Allow-Origin": "*" 
        }
            }
