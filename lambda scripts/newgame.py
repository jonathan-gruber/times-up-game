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

def deleteallwords(event, context):
    dynamodb = boto3.resource('dynamodb')

    scoretable = dynamodb.Table('timesup-score')
    scoreresponse = scoretable.scan(
    )
    print(scoreresponse)
    for teamz in scoreresponse['Items']:
        print("teamzzzz")
        print(teamz["team"])
        teamsupdate = scoretable.update_item(
            Key={
                'team': teamz["team"]
            },
            UpdateExpression='SET #VALUE = :free',
            ExpressionAttributeNames={
                '#VALUE': 'score',
            },
            ExpressionAttributeValues={
                ':free': 0
            },
            ReturnValues='UPDATED_NEW'
        )

    table = dynamodb.Table('timesup-words')
    response = table.scan(
    )
    print(response)
    for wordz in response['Items']:
        print("wordzzzz")
        print(wordz["word"])
        response2 = table.delete_item(
            Key={
                'word': wordz["word"]
            }
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
