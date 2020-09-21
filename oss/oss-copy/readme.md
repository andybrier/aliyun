# oss copy

`oss`设置加密只会对新`PUT`到`bucket`中的对象加密。 如何对以前`put`的数据加密呢？ 

 - step 0: 配置`bucket`的加密. [参考](https://help.aliyun.com/document_detail/31871.html?spm=a2c4g.11186623.6.695.7dc755f7NaRrfU)
 - step 1 : 生成`oss`的清单文件. 参考[链接](https://help.aliyun.com/document_detail/163489.html?spm=5176.10695662.1996646101.searchclickresult.10362c6fvGPYU3)。 注意`清单文件可选信息` 选择所有的信息，包括 `文件大小`、`etag`、`加密状态等`
 - step 2: 运行， 修改并且运行`oss-copy.py` 主要包括`access_key`, `access_secret`, `manifest_url`，`bucket_name`等。 
 
 ```python
 pip install oss2
 python oss-copy.py <目录>

 # 无目录
 python oss-copy.py  NULL-DIR    
 ```

 注意：
  >
  > 如果bucket设置了多版本，则会生成新版本的文件，否则会覆盖原来版本的文件。[参考](https://help.aliyun.com/document_detail/118923.html?spm=a2c4g.11186623.6.935.79045a98RR5pi1)
  >
  > 大于`1G`的文件不会处理
  >
  > `manifest_url` 是生成的清单文件的元文件。 [参考](https://help.aliyun.com/document_detail/163489.html?spm=5176.11065259.1996646101.searchclickresult.114515a7Xbjpbr)
 