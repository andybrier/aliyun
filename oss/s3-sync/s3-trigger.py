import boto3
import json
import oss2
import subprocess
import urllib



#aws sqs
region_name = 'ap-east-1'
queue_name = 's3-to-oss'
max_queue_messages = 10
aws_access_key_id = 'AKIARJH'
aws_secret_access_key = 'YodFIlyYpIgRqu7HtSwDIW'
sqs = boto3.resource('sqs', region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)


#aliyun
access_key = 'LTAI4G6hKB'
access_secret = 'oAOIjO7aa6'
# bucket name
bucket_name = 'bucketName'
# endpoint for bucket
domain = 'http://oss-cn-beijing.aliyuncs.com'
auth = oss2.Auth(access_key,  access_secret)
oss_bucket = oss2.Bucket(auth, domain, bucket_name)



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
            try:
                if record['eventName'] == 'ObjectCreated:Put' and record['eventSource'] == 'aws:s3':
                    bucket = record['s3']['bucket']['name']
                    #print(record['s3']['object']['key'])
                    print(record)
                    key = urllib.unquote_plus(record['s3']['object']['key'].encode('utf8'))
                    lastname = key.split("/")[-1]
                    local = '/tmp/' + lastname
                    #print('local: %s, key: %s, bucket: %s' %(local, key, bucket))
                    s3.download_file(Filename=local, Key=key, Bucket=bucket)
                    #upload
                    oss_bucket.put_object_from_file(key, local)
                    #remove
                    subprocess.call('rm %s' %local, shell=True)

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
