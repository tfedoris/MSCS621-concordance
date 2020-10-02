import boto3

def create_location_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8080")

    table = dynamodb.create_table(
        TableName='Locations'
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
                'AttributeName': 'location'
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
    location_table = create_location_table()
    print("Table status:", location_table.table_status)