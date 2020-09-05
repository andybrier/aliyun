# -*- coding: utf-8 -*-
import oss2
import csv
import urlparse
import subprocess
import os
import json

# access key and secret
access_key = 'LTR'
access_secret = 'f6RD6S'
# bucket name
bucket_name = 'mybucket'
# endpoint for bucket
domain = 'http://oss-cn-beijing.aliyuncs.com'
#bucket inventory menifest file path
manifest_url = 'https://mybucket.oss-cn-beijing.aliyuncs.com/mybucket/all/2020-09-03T06-42Z/manifest.json'

# proccess single csv file
def process(inventory):
  auth = oss2.Auth(access_key,  access_secret)
  bucket = oss2.Bucket(auth, domain, bucket_name)
  with open(inventory) as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',')
      line_count = 0
      for row in csv_reader:
          key = urlparse.unquote(row[1])
          enc_status = row[7]
          if int(row[2]) > 1073741824 :
            print("file %s is too large." %key)
            continue
          if(enc_status == 'FALSE' or enc_status == 'false'):
              bucket.copy_object(bucket_name, key, key)
          line_count = line_count + 1
          print(".")

def main():
  #download manifest file 
  menifest_file_name = manifest_url.split("/")[-1]
  cmd='wget -O %s %s' % (menifest_file_name, manifest_url)
  subprocess.call(cmd, shell=True)
  print("success get menifest file: %s" %manifest_url)
  # https://andybrier.oss-cn-beijing.aliyuncs.com'
  host =  urlparse.urlparse(manifest_url).scheme + "://" + urlparse.urlparse(manifest_url).hostname
  with open( menifest_file_name,'r') as menifest:
        m_json = json.load(menifest)
        for csv_file in m_json['files']:
          #download inventory gzip file:  xxxx.csv.gz
          local_gz_file = csv_file['key'].split("/")[-1]
          down_csv_cmd = 'wget -O %s %s' % (local_gz_file, host + '/' + csv_file['key'])
          subprocess.call(down_csv_cmd, shell=True)
          #gzip
          ugzip = 'gzip -d %s' %local_gz_file
          subprocess.call(ugzip, shell=True)
          #final inventory csv file: xxxx.csv
          inventory =  os.path.splitext(local_gz_file)[0]
          print("start to proccess file: %s" %inventory)
          process(inventory)
          print("success proccessed file: %s" %inventory)
          subprocess.call('rm %s' %inventory, shell=True)



if __name__ == "__main__":
    main()


		

 