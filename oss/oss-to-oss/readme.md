# 安装

## 安装`python 2.7` , `pip`

## 安装

``` 
# install virtulenv
yum install python-virtualenv

#active virtualenv
mkdir oss-to-oss
cd oss-to-oss
python -m virtualenv venv
. venv/bin/activate

#install 
pip install Flask
pip install waitress
pip install boto3==1.17.48
pip install oss2
```


## copy
 把文件 `app.py`复制到目录 `oss-to-oss`中

## 运行python
 - 准备`OSS`的`RAM`子账号的`AK/SK`, 注意 `AK/SK`需要有`OSS`写的权限 
 - 修改 `app.py` 中相关的配置，详细见注释
 - 运行：`python app.py &`

## 配置源OSS的事件通知
- 基础设置 --> 事件通知 -->设置 -->创建规则 
- 事件类型： `PutObject`, `CopyObject`, `PostObject`
- 资源描述： `前后缀`，都留空即可
- 接收终端： `http://IP/oss/notify'`


see: https://help.aliyun.com/document_detail/122379.html?spm=a2c4g.11174283.6.837.32847da2TgJRHI

 

