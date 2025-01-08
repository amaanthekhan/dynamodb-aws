import boto3

dynamodb = boto3.resource('dynamodb',region_name='us-east-1')

table = dynamodb.create_table(
    TableName='employee',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'N'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    },
)

print("Table status", table.table_status)

table.put_item(
    Item={
        'id': 1,
        'name': 'ABC',
        'salary': 20000
    },
)
table.put_item(
    Item={
        'id': 2,
        'name': 'DEF',
        'salary': 22000
    },
)
table.put_item(
    Item={
        'id': 3,
        'name': 'XYZ',
        'salary': 25000
    },
)