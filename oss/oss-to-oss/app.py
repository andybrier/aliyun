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

####################################### CHNAGE THIS #######################################
# auth info for source oss
src_auth = { 'access_key' : '',   'access_secret' :  ''}

# auth info for destination oss
dst_auth = { 'access_key' : '',   'access_secret' :  ''}

# src bucket --> dst bucket
bucket_mappings = {'SRC_BUCKET' :  'DST_BUCKET' }

# bucket endpoint mappings
bucket_domain_mappings =  {'SRC_BUCKET' : 'oss-cn-beijing.aliyuncs.com',  
                           'DST_BUCKET': 'oss-us-west-1.aliyuncs.com'}

####################################### CHNAGE THIS #######################################


def download_from_oss(bucket_name, object_key):

    access_key = src_auth['access_key']
    access_secret = src_auth['access_secret']
    domain =  bucket_domain_mappings[bucket_name]
    auth = oss2.Auth(access_key,  access_secret)
    bucket = oss2.Bucket(auth, domain, bucket_name)

    #save to local
    key = urllib.unquote_plus(object_key.encode('utf8'))
    lastname = key.split("/")[-1]
    local = '/tmp/' + lastname
    bucket.get_object_to_file(key, local)
    return local

def upload_to_oss(src_bucket_name,object_key,local_file):
    
    access_key = dst_auth['access_key']
    access_secret = dst_auth['access_secret']
    dst_bucket = bucket_mappings[src_bucket_name]
    domain =   bucket_domain_mappings[dst_bucket]
    auth = oss2.Auth(access_key,  access_secret)
    bucket = oss2.Bucket(auth, domain, dst_bucket)

    #upload to oss
    key = urllib.unquote_plus(object_key.encode('utf8'))
    bucket.put_object_from_file(key, local_file)


app = Flask(__name__)
@app.route('/oss/notify',  methods=['POST'])
def oss_notify():
   data = base64.b64decode(request.data)
   body = json.loads(data)
   for event in body['events']:
     bucket_name = event['oss']['bucket']['name']
     key = event['oss']['object']['key']
     local = download_from_oss(bucket_name, key)
     upload_to_oss(bucket_name,   key, local)
     subprocess.call('rm %s' %local, shell=True)
   return 'Server is OK'

if __name__ == '__main__':
  from waitress import serve
  serve(app, host="0.0.0.0", port=80)