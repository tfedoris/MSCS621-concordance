import boto3

def create_location_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName='Locations',
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
    return table

if __name__ == '__main__':
    location_table = create_location_table()
    location_table.meta.client.get_waiter('table_exists').wait(TableName='Locations')
    print("Table status:", location_table.table_status)