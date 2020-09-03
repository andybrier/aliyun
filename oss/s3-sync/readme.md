# s3 实时同步到 oss

方案：
 - put object into s3
 - trigger `lambda`
 - call server's http api, send `key` and `domain` 
 - server download the file by `domain` and `key`
 - server put the object into oss