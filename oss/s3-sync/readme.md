# s3 实时同步到 oss

方案：
 - put object into s3
 - trigger `lambda`
 - call server's http api, send `key` and `domain` 
 - server download the file by `domain` and `key`
 - server put the object into oss



 SQS Policy

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


 创建一个ec2访问sqs的role：  ec2-read-sqs-role


Access key ID    AKIAT6B4D6Q4WKFK4RJH
Secret access key   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


```json

{
  "Records": [
    {
      "eventVersion": "2.1",
      "eventSource": "aws:s3",
      "awsRegion": "ap-east-1",
      "eventTime": "2020-09-14T05:31:50.329Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "AW0C5LIQ7QYNI"
      },
      "requestParameters": {
        "sourceIPAddress": "47.251.4.198"
      },
      "responseElements": {
        "x-amz-request-id": "4F17BD3B5AF27799",
        "x-amz-id-2": "ohC5lwTFVpCR6VaqqSaRN+gV4axzt5usMm6W5TbgUsJL+CWopUDDbgjezJTIn36ty51iyroCcLYJUPgatygSnBvV2hdcVxl3"
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "sss",
        "bucket": {
          "name": "hk-bucket-huachun",
          "ownerIdentity": {
            "principalId": "AW0C5LIQ7QYNI"
          },
          "arn": "arn:aws:s3:::hk-bucket-huachun"
        },
        "object": {
          "key": "aa.txt",
          "size": 6,
          "eTag": "5a2a525d0ccf28ee9d2d6748ec0f3f0c",
          "sequencer": "005F5F00497AE2D491"
        }
      }
    }
  ]
}

```


[OSS 本地文件上传](https://help.aliyun.com/document_detail/32027.html)
