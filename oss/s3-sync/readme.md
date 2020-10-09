# Sync object from aws s3 to aliyun oss in time

How：
 - put object into `s3`
 - trigger event into `SNS`
 - subscribe `SNS` topic and put message into `SQS`
 - listen to `SQS` and download the object, then put the object into aliyun `oss`


 ##  Policy: 

`S3-to-SNS` Policy

```
{
  "Id": "Policy1602226397417",
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1602226396682",
      "Action": [
        "sns:Publish"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:sns:us-west-2:7905:<SNS>",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "arn:aws:s3:::<buckect>"
        }
      },
      "Principal": "*"
    }
  ]
}
```


`SNS-to-SQS` policy
 ```
{
  "Id": "Policy1602226238398",
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1602225506333",
      "Action": [
        "sqs:SendMessage"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:sqs:us-west-2:79365:<SQS>",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "arn:aws:sns:us-west-2:71905:<SNS>"
        }
      },
      "Principal": "*"
    }
  ]
}

 ```
 
 AWS Key :
  - download from `s3`
  - subscribe and pull messages from `sqs`
  
  Aliyun Key:
  - upload into `oss`
 

 ref:  [为通知配置一个存储区（SNS主题或SQS队列）](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/dev/ways-to-add-notification-config-to-bucket.html)
 



 ## AWS `IAM` for receive message from `SQS` 

Retrive message from aws `SQS`



## send object into aliyun `oss`

[OSS 本地文件上传](https://help.aliyun.com/document_detail/32027.html)
