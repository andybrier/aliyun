# -*- coding: utf-8 -*-
# doc: https://help.aliyun.com/document_detail/122379.html?spm=a2c4g.11174283.6.837.32847da2TgJRHI

from flask import Flask
from flask import request
import boto3
import base64
import json
import oss2
import subprocess
import urllib


def download_from_oss(bucket_name, object_key):
    ########## MODIFY THIS #############
    #key, secret [AliyunOSSReadOnlyAccess]
    access_key = ''
    access_secret = ''
    #and oss domain
    domain = 'oss-cn-hangzhou-internal.aliyuncs.com'
    ##############################
    auth = oss2.Auth(access_key,  access_secret)
    bucket = oss2.Bucket(auth, domain, bucket_name)

    #save to local
    key = urllib.unquote_plus(object_key.encode('utf8'))
    lastname = key.split("/")[-1]
    local = '/tmp/' + lastname
    bucket.get_object_to_file(key, local)
    return local

def upload_to_s3(bucket,key,local_file):
    ###########  MODIFY THIS ##########
    #key, secret [AmazonS3FullAccess]
    aws_access_key_id = ''
    aws_secret_access_key = ''
    region_name = 'ap-east-1'
    ##############################
    from boto3.session import Session
    session = Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
    s3 = session.client("s3")
    #upload to s3
    clean_key =  urllib.unquote_plus(key.encode('utf8'))
    s3.upload_file(local_file, bucket,clean_key)



app = Flask(__name__)
@app.route('/oss/notify',  methods=['POST'])
def oss_notify():
   data = base64.b64decode(request.data)
   body = json.loads(data)
   for event in body['events'] ： 
     bucket_name = event['oss']['bucket']['name']
     key = event['oss']['object']['key']
     local = download_from_oss(bucket_name, key)
     upload_to_s3(bucket_name,   key, local)
     subprocess.call('rm %s' %local, shell=True)
   return 'Hello World'

if __name__ == '__main__':
  from waitress import serve
  serve(app, host="0.0.0.0", port=80)