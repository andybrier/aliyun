import boto3
import json

#aws sqs
region_name = 'ap-east-1'
queue_name = 's3-to-oss'
max_queue_messages = 10
aws_access_key_id = 'AKIAFK4RJH'
aws_secret_access_key = 'YodFIlZHtSwDIW'
sqs = boto3.resource('sqs', region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)


#aliyun
access_key = 'LTR'
access_secret = 'f6RD6S'
# bucket name
bucket_name = 'mybucket'
# endpoint for bucket
domain = 'http://oss-cn-beijing.aliyuncs.com'


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
        if 'Records' in body:
          for record in body['Records']:
            if record['eventName'] == 'ObjectCreated:Put' and record['eventSource'] == 'aws:s3':
              bucket = record['s3']['bucket']['name']
              key = record['s3']['object']['key']
              lastname = key.split("/")[-1]
              s3.download_file(Filename='/tmp/' + lastname, Key=key, Bucket=bucket)
              #upload






        # add message to delete
        messages_to_delete.append({
            'Id': message.message_id,
            'ReceiptHandle': message.receipt_handle
        })

    # if you don't receive any notifications the
    # messages_to_delete list will be empty
    if len(messages_to_delete) == 0:
        break
    # delete messages to remove them from SQS queue
    # handle any errors
    else:
        delete_response = queue.delete_messages(
                Entries=messages_to_delete)
