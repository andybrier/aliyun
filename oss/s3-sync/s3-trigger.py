import json
from botocore.vendored import requests

def lambda_handler(event, context):
 # event contains all information about uploaded object
   print("Event :", event)

   # Bucket Name where file was uploaded
   source_bucket_name = event['Records'][0]['s3']['bucket']['name']

   # Filename of object (with path)
   file_key_name = event['Records'][0]['s3']['object']['key']
   

   # Copy Source Object
   # change domain
   # change key :  dd.jpg
   payload = {'domain': 'https://static.mysmth.net', 'key': 'nForum/img/legal/hdfj.jpg'}
   #payload = {'domain': 'http://andybrier-logs.s3-us-west-2.amazonaws.com/', 'key': file_key_name}
   r = requests.get('http://server/awsnotify', params=payload)

   # S3 copy object operation
   #s3_client.copy_object(CopySource=copy_source_object, Bucket=destination_bucket_name, Key=file_key_name)
   


   return {
       'statusCode': r.status_code,
       'body': r.text
   }
