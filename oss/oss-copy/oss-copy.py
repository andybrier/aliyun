# -*- coding: utf-8 -*-
import oss2
import csv

access_key = 'LT4R'
access_secret = 'f66S'
inventory = 'bff9c70d-45c6-4dfe-98ca-e37faeb5a001.csv'
bucket_name = 'mybucket'
domain = 'http://oss-cn-beijing.aliyuncs.com'

# 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
auth = oss2.Auth(access_key,  access_secret)
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, domain, bucket_name)


with open(inventory) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
         key = row[1]
         enc_status = row[7]
         if row[2] >= 1073741824 :
           continue
         if(enc_status == 'FALSE' or enc_status == 'false'):
             bucket.copy_object(bucket_name, key, key)
         line_count = line_count + 1
         print('%d' %line_count)
