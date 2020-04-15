import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def add_word(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('timesup-words')
    query_param = event['queryStringParameters']
    newword = query_param['newword']

    response = table.put_item(
        Item={
            'word':newword, 
            'free': 'yes'
        }
        )

    response3 = table.scan(
    )
    
    print("PutItem succeeded:")
#print(table.item_count)
    body_response = json.dumps(response3, indent=4, cls=DecimalEncoder)

    return {
        "statusCode": 200,
        "body": body_response, 
                "headers": { 
            "Access-Control-Allow-Origin": "*" 
        }
            }

