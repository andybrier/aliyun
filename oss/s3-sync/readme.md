# s3 实时同步到 oss

方案：
 - put object into `s3`
 - trigger event into `SQS` 
 - listen to `SQS` and download the object, then put the object into aliyun `oss`


 ## SQS Policy: 
`S3`  `PUT` event to `SQS`

 ```json
{
  "Version": "2008-10-17",
  "Id": "__default_policy_ID",
  "Statement": [
    {
      "Sid": "__owner_statement",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::270709027897:root"
      },
      "Action": "SQS:*",
      "Resource": "arn:aws:sqs:ap-east-1:270709027897:s3-to-oss"
    },
    {
      "Sid": "__sender_statement",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "SQS:SendMessage",
      "Resource": "arn:aws:sqs:ap-east-1:270709027897:s3-to-oss",
      "Condition": {
        "StringEquals": {
          "aws:SourceAccount": "270709027897"
        },
        "ArnLike": {
          "aws:SourceArn": "arn:aws:s3:::hk-bucket-huachun"
        }
      }
    },
    {
      "Sid": "__receiver_statement",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::270709027897:role/ec2-read-sqs-role"
      },
      "Action": [
        "SQS:ChangeMessageVisibility",
        "SQS:DeleteMessage",
        "SQS:ReceiveMessage"
      ],
      "Resource": "arn:aws:sqs:ap-east-1:270709027897:s3-to-oss"
    }
  ]
}


 ```

 ref:  [为通知配置一个存储区（SNS主题或SQS队列）](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/dev/ways-to-add-notification-config-to-bucket.html)
 



 ## AWS `IAM` for receive message from `SQS` 

Retrive message from aws `SQS`


## send object into aliyun `oss`

[OSS 本地文件上传](https://help.aliyun.com/document_detail/32027.html)
