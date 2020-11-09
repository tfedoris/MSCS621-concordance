import boto3
import json

from swagger_server.models.result import Result
from swagger_server.models.result_concordance import ResultConcordance

dynamodb = boto3.client('dynamodb', region_name='us-east-2')

def create_concordance_table():
    table_name = 'concordance'
    existing_tables = dynamodb.list_tables()['TableNames']

    if table_name not in existing_tables:
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'input',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'input',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

def upload_concordance_data(result):
    concordance_maps = []

    for result_concordance in result.concordance:
        result_dict = result_concordance.to_dict()
        concordance_maps.append({
            'M': {
                'token': {'S': result_dict['token']},
                'count': {'N': json.dumps(result_dict['count'])}
            }
        })

    resource = boto3.resource('dynamodb', region_name='us-east-2')
    get_response = resource.Table('concordance').get_item(Key={'input': result.input})

    if 'Item' not in get_response:
        concordance_item = {
            'input':{'S':result.input},
            'concordance':{'L':concordance_maps}
        }
        print(concordance_item)
        response = dynamodb.put_item(
            TableName='concordance',
            Item=concordance_item
        )
        print("UPLOADING ITEM")
        print(response)