from flask import Flask, request
import requests
import json
import oss2
import urllib

app = Flask(__name__)

@app.route('/')
def s3ToOss():
 key= request.args.get('key')
 domain = request.args.get('domain')
 url = domain + '/' + key
 print(url)
 r = requests.get('http://100.100.100.200/latest/meta-data/Ram/security-credentials/ecs-to-oss')
 token = json.loads(r.text)
 endpoint = 'oss-cn-hangzhou.aliyuncs.com'
 auth = oss2.StsAuth(token['AccessKeyId'], token['AccessKeySecret'], token['SecurityToken'])
 bucket = oss2.Bucket(auth, endpoint, 'andybrier-bucket2')


 pic = urllib.urlopen(url)
    # Store all the pictures in oss bucket, keyed by timestamp in microsecond unit
    #bucket.put_object('xxx.txt', 'Ali Baba is a happy youth.')
 bucket.put_object(key, pic)

 return"Hello World!"

if __name__ == '__main__':
 app.run(port = 5000)