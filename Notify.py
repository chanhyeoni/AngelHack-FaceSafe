from __future__ import print_function

import boto3
from decimal import Decimal
import json
import httplib, urllib, time

print('Loading function')

rekognition = boto3.client('rekognition')

PUSHOVER_USERKEY = "PUSHOVER_USERKEY"
PUSHOVER_APIKEY = "PUSHOVER_APIKEY"
def alert(title, messages):
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST","/1/messages.json",
            urllib.urlencode({
                "token": PUSHOVER_APIKEY,
                "user":PUSHOVER_USERKEY ,
                "title":title,
                "message": messages,
                "priority":1,
                "timestamp":int(time.time()),
                #'sound': sound
                }),{"Content-type":"application/x-www-form-urlencoded"})
    conn.getresponse()
# --------------- Helper Functions to call Rekognition APIs ------------------




def detect_labels(bucket, key):
    response = rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    # Sample code to write response to DynamoDB table 'MyTable' with 'PK' as Primary Key.
    # Note: role used for executing this Lambda function should have write access to the table.
    #table = boto3.resource('dynamodb').Table('MyTable')
    #labels = [{'Confidence': Decimal(str(label_prediction['Confidence'])), 'Name': label_prediction['Name']} for label_prediction in response['Labels']]
    #table.put_item(Item={'PK': key, 'Labels': labels})
    return response

def search_faces_by_image(bucket, key):
    # try:
    response = rekognition.search_faces_by_image(Image={"S3Object": {"Bucket": bucket, "Name": key}}, CollectionId="friends", FaceMatchThreshold=0.9001)
    alert("Alert", "https://s3.amazonaws.com/datasetfacerec/" + key)
    if response["SearchedFaceConfidence"] > 0.9001:
        if len(response["FaceMatches"]) is 0 : 
            alert("Alert", "https://s3.amazonaws.com/datasetfacerec/" + key)
    return response
    # except InvalidParameterException as e:
    #     return None

# --------------- Main handler ------------------


def lambda_handler(event, context):
    '''Demonstrates S3 trigger that uses
    Rekognition APIs to detect faces, labels and index faces in S3 Object.
    '''
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        response = search_faces_by_image(bucket, key)
        # Print response to console.
        print(response)

        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e
