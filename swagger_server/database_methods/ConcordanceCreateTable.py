import boto3

def create_concordance_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName='Concordance',
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
    concordance_table = create_concordance_table()
    concordance_table.meta.client.get_waiter('table_exists').wait(TableName='Concordance')
    print("Table status:", concordance_table.table_status)