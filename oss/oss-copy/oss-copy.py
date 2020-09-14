# -*- coding: utf-8 -*-
import oss2
import csv
import urlparse
import subprocess
import os
import json
import sys

# access key and secret
access_key = 'LTR'
access_secret = 'f6RD6S'
# bucket name
bucket_name = 'mybucket'
# endpoint for bucket
domain = 'http://oss-cn-beijing.aliyuncs.com'
#bucket inventory menifest file path
manifest_url = 'https://mybucket.oss-cn-beijing.aliyuncs.com/mybucket/all/2020-09-03T06-42Z/manifest.json'

auth = oss2.Auth(access_key,  access_secret)
bucket = oss2.Bucket(auth, domain, bucket_name)


directory = ''
if len(sys.argv) > 1:
  directory = sys.argv[1]

print(directory)

# proccess single csv file
def process(inventory):

  with open(inventory) as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',')
      line_count = 0
      for row in csv_reader:
          key = urlparse.unquote(row[1])
          if (directory != '' ) and (not key.startswith(directory)):
            continue
          enc_status = row[7]
          if int(row[2]) > 1073741824 :
            print("file %s is too large." %key)
            continue
          if(enc_status == 'FALSE' or enc_status == 'false'):
              bucket.copy_object(bucket_name, key, key)
          line_count = line_count + 1
          print(".")

def main():
  #down load manifest file 
  menifest_file_name = manifest_url.split("/")[-1]
  bucket.get_object_to_file(urlparse.urlparse(manifest_url).path.lstrip('/'), menifest_file_name)
  
  print("success get menifest file: %s" %manifest_url)
  # https://andybrier.oss-cn-beijing.aliyuncs.com'
  with open( menifest_file_name,'r') as menifest:
        m_json = json.load(menifest)
        for csv_file in m_json['files']:
          local_gz_file = csv_file['key'].split("/")[-1]
          bucket.get_object_to_file(csv_file['key'], local_gz_file)
          #gzip
          ugzip = 'gzip -d %s' %local_gz_file
          subprocess.call(ugzip, shell=True)
          inventory =  os.path.splitext(local_gz_file)[0]
          print("start to proccess file: %s" %inventory)
          process(inventory)
          print("success proccessed file: %s" %inventory)
          subprocess.call('rm %s' %inventory, shell=True)



if __name__ == "__main__":
    main()
