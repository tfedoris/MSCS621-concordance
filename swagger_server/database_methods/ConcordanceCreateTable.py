import boto3

def create_concordance_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8080")

    table = dynamodb.create_table(
        TableName='Concordance'
        KeySchema=[
            {
                'AttributeName': 'input',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'token'
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'count'
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

if __name__ == '__main__':
    concordance_table = create_concordance_table()
    print("Table status:", concordance_table.table_status)