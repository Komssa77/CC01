import json
import boto3
import keys_config as keys
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import requests
import os

#https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html


__TableName__ = "Users"
Primary_Column_Name = 'UserID'
columns=["Username","Password"]

iam_client = boto3.client('iam')
responseIAM = iam_client.list_users()
#print(responseIAM)


#dynamodb_client = boto3.client('dynamodb', region_name='ap-southeast-2')
#responseDB = dynamodb_client.list_tables()
#print(responseDB['TableNames'])




#creating the user table
def depreciate():
    dynamodb_client = boto3.resource('dynamodb', region_name='ap-southeast-2')

    try: 
        newTable = dynamodb_client.create_table(
            TableName='depreciate',
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
        print("complete")
        #initItems()

    except dynamodb_client.exceptions.ResourceInUseException:
        print("users table already exists")






def initFunctions():
    dynamodb_client = boto3.client('dynamodb', region_name='ap-southeast-2')
    responseDB = dynamodb_client.list_tables()
    #print(responseDB)

    if 'Init_users' not in responseDB['TableNames']:
        createTableUsers()
    else:
        print("user table already initialized")

    if 'music' not in responseDB['TableNames']:
        createTableMusic()
    else:
        print("music table already initialized")
    
    #s3UploadingInit() #uploads all initial images




def createTableUsers():
    dynamodb_client = boto3.resource('dynamodb', region_name='ap-southeast-2')

    
    newTable = dynamodb_client.create_table(
        TableName='Init_users',
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
           
        ],
    ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
        )

    newTable.wait_until_exists()
    print("user table created")
    initItemsUsers()



'https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html'

def initItemsUsers():

    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('Init_users')
    initItemsList=[{
            'username': 'CF0',
            'email': 's37814750@student.rmit.edu.au',
            'password': '012345',
        },{
            'username': 'CF1',
            'email': 's37814751@student.rmit.edu.au',
            'password': '123456',
        },{
            'username': 'CF2',
            'email': 's37814752@student.rmit.edu.au',
            'password': '234567',
        },{
            'username': 'CF3',
            'email': 's37814753@student.rmit.edu.au',
            'password': '345678',
        },{
            'username': 'CF4',
            'email': 's37814754@student.rmit.edu.au',
            'password': '456789',
        },{
            'username': 'CF5',
            'email': 's37814755@student.rmit.edu.au',
            'password': '567890',
        },{
            'username': 'CF6',
            'email': 's37814756@student.rmit.edu.au',
            'password': '678901',
        },{
            'username': 'CF7',
            'email': 's37814757@student.rmit.edu.au',
            'password': '789012',
        },{
            'username': 'CF8',
            'email': 's37814758@student.rmit.edu.au',
            'password': '890123',
        },{
            'username': 'CF9',
            'email': 's37814759@student.rmit.edu.au',
            'password': '901234',
        }
        ]
    
    for item in initItemsList:
        table.put_item(Item = item)
    
    print("user table items initialized")




def createTableMusic():
    dynamodb_client = boto3.resource('dynamodb', region_name='ap-southeast-2')

    
    newTable = dynamodb_client.create_table(
        TableName='music',
        KeySchema=[
            {
                'AttributeName': 'title',
                'KeyType': 'HASH'  # HASH for the primary key
            },
            {
                'AttributeName': 'artist',
                'KeyType': 'RANGE'  # RANGE for the sort key
            },
        ],
    AttributeDefinitions=[
            {
                'AttributeName': 'title',
                'AttributeType': 'S'  # S for String type
            },
            {
                'AttributeName': 'artist',
                'AttributeType': 'S'  # S for String type
            },
           
        ],
    ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
        )

    newTable.wait_until_exists()
    print("music table created")
    initItemsMusic()




def initItemsMusic():
    
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('music')

    jsonFile = open('a1.json')
    musicData = json.load(jsonFile)#here
    jsonFile.close()
    
    with table.batch_writer() as batch:
        for item in musicData['songs']:
            batch.put_item(Item = item)
    
    print("music items initialized")



#https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python
#https://stackoverflow.com/questions/30229231/python-save-image-from-url

def s3UploadingInit():
    s3_Client = boto3.client('s3')
    response = s3_Client.list_buckets()

    print('Buckets:')
    for x in response['Buckets']:
        print('     ' + x['Name'])

    bucketName = 'test-bucket-komssa'

    jsonFile = open('a1.json')
    musicData = json.load(jsonFile)#here
    jsonFile.close()

    for x in musicData['songs']:
        
        #print(x)
        img_data = requests.get(x['img_url']).content
        object_name = os.path.basename(x['img_url'])
                                       
        with open('ImageTemp/' + object_name, 'wb') as handler:
            handler.write(img_data)

        if object_name is None:
            object_name = os.path.basename('Mori2') #changes name of file
        
        #more to be done
        try:
            response = s3_Client.upload_file('ImageTemp/' + object_name, bucketName, os.path.basename(x['img_url']))
            print('uploaded image ' + object_name)

        except ClientError as e:
            print('Broken')




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



def checkLoginDetails(emailInput, passwordInput):
    
    dynamodb_resource = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb_resource.Table("Init_users")

    print("checking email: " + emailInput)
    # Perform the query operation
    response = table.scan(
        #KeyConditionExpression=Key('email').eq(emailInput)
        FilterExpression=Attr('email').eq(emailInput)
    )
    
    if (response['Count'] == 1):
        print(response['Items'])
        x = response['Items'][0]
        if x['password'] == passwordInput:
            print("Login successful!")
            return True
        else:
            print("Login failed. Username or password incorrect.")
            return False
    else:
        print("Login failed. Username or password incorrect.")
        return False

def new():
    myWords = ["Not","everything","that","counts","can","be","counted","and","not","everything","that","can","be","counted","counts"]
    count = len(myWords)

    if count % 2 == 1: #odd
        point = int ((count-1)/2)

        print(myWords[:point])
        print(myWords[point:])

    else: # even
        point = int (count/2)

        print(myWords[:point])
        print(myWords[point:])


    mid = len(myWords) // 2
    print(myWords[:mid])
    print(myWords[mid:])

#checkLoginDetails('User1','Pass2')
initFunctions()
#new()
