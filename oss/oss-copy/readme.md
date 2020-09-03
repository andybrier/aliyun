# oss copy

`oss`设置加密只会对新`PUT`到`bucket`中的对象加密。 如何对以前`put`的数据加密呢？ 

 - step 1 : 生成`oss`的清单文件. 参考[链接](https://help.aliyun.com/document_detail/163489.html?spm=5176.10695662.1996646101.searchclickresult.10362c6fvGPYU3)。 注意`清单文件可选信息` 选择所有的信息，包括“文件大小、etag、加密状态等”
 - step 2: 下载清单文件。 如果`bucket`文件比较多，可能需要一定的时间生成。 生成成功之后，可以在设置目录的类似位置 `/data/bff9c70d-45c6-4dfe-98ca-e37faeb5a001.csv.gz` 下载清单文件
 - step 3: 解压，并且将这个`csv`文件和`python`文件放在一个目录下
 - step 4: 运行， 修改`oss-copy.py` 主要包括`access_key`, `access_secret`, `inventory`，`bucket_name`等。 并且运行
 
 ```python
 pip install oss2
 python oss-copy.py
 ```

 注意：
  >
  > 如果bucket设置了多版本，则会生成新版本的文件，否则会覆盖原来版本的文件。[参考](https://help.aliyun.com/document_detail/118923.html?spm=a2c4g.11186623.6.935.79045a98RR5pi1)
  >
 