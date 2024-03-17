import boto3
import keys_config as keys


#https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html


__TableName__ = "Users"
Primary_Column_Name = 'UserID'
columns=["Username","Password"]

iam_client = boto3.client('iam')
responseIAM = iam_client.list_users()
#print(responseIAM)


dynamodb_client = boto3.client('dynamodb', region_name='ap-southeast-2')
responseDB = dynamodb_client.list_tables()
print(responseDB['TableNames'])





def createTable():
    dynamodb_client = boto3.resource('dynamodb', region_name='ap-southeast-2')
    newTable = dynamodb_client.create_table(
        TableName='users',
        KeySchema=[
        {
            'AttributeName': 'username',
            'KeyType': 'HASH'  # HASH for the primary key
        },
        {
            'AttributeName': 'email',
            'KeyType': 'RANGE'  # RANGE for the sort key
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'username',
            'AttributeType': 'S'  # S for String type
        },
        {
            'AttributeName': 'email',
            'AttributeType': 'S'  # S for String type
        },
        #{
        #    'AttributeName': 'password',
        #    'AttributeType': 'S'  # S for String type
        #}
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
    )

    newTable.wait_until_exists()
    print(newTable.item_count)
    





def CheckingID():

    dynamodb_resource = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb_resource.Table(__TableName__)

    response = table.get_item(
        Key={
            'UserID': "1"
        }
    )

    if 'Item' in response:
        details = response['Item']
        print(details)
        print("GOOD")
        print("Username:", details['Username'])
        print("Password:", details['Password'])
    else:
        print('not found')




def addingElements():
    dynamodb_resource = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table_name = 'Users'
    table = dynamodb_resource.Table(table_name)
    items_to_insert = [
        {
            'UserID': '3',
            'Password': 'Pass1',
            'Username': 'User3'
        },
        {
            'UserID': '4',
            'Password': 'Pass2',
            'Username': 'User45'
        }
    ]

    for item in items_to_insert:
        table.put_item(Item=item)



def checkLoginDetails(usernameInput, passwordInput):
    
    dynamodb_resource = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb_resource.Table("Users")

    # Perform the query operation
    response = table.scan(
        FilterExpression='Username = :username',
        ExpressionAttributeValues={
            ':username': usernameInput
        }
    )

    #print(response)
    if response['Count'] > 0:
        info = response['Items'][0]
        #print(info)
        #print(info['Password'])

        if info['Password'] == passwordInput:
            print("Login successful!")
            return True
        else:
            print("Login failed. Username or password incorrect.")
            return False
    else:
        return False


checkLoginDetails('User1','Pass2')
createTable()