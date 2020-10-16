import boto3
import json
import oss2
import subprocess
import urllib
import sys


#aws sqs
region_name = 'ap-east-1'
queue_name = 's3-to-oss'
aws_access_key_id = 'AKIARJH'
aws_secret_access_key = 'YodFIlyYpIgRqu7HtSwDIW'
sqs = boto3.resource('sqs', region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)
max_queue_messages = 10


# we only need to care abount messages from those buckets
buckets = ['imagemanage', 'mallfile-storage']



from boto3.session import Session
session = Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
s3 = session.client("s3")


queue = sqs.get_queue_by_name(QueueName=queue_name)
while True:
    messages_to_delete = []
    for message in queue.receive_messages(
            MaxNumberOfMessages=max_queue_messages):
        # process message body
        body = json.loads(message.body)
        #print("receive: %s" %body)
        if 'Records' in body:
          for record in body['Records']:
            bucket = record['s3']['bucket']['name']
            try:
                if bucket not in buckets:  
                    #delete message
                    messages_to_delete.append({
                        'Id': message.message_id,
                        'ReceiptHandle': message.receipt_handle
                    })
            except:
                print("error happened when proccessing: %s"  %record)

    if len(messages_to_delete) > 0:
      delete_response = queue.delete_messages(
                Entries=messages_to_delete)
