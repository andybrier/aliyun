# how to install

## install python v2.7

## install virtualenv

``` 
# install virtulenv
yum install python-virtualenv

#active virtualenv
mkdir oss-to-s3
cd oss-to-s3
python -m virtualenv venv
. venv/bin/activate

#install 
pip install Flask
pip install waitress
pip install boto3
pip install oss2
```


# set up notify for aliyun oss

see: https://help.aliyun.com/document_detail/122379.html?spm=a2c4g.11174283.6.837.32847da2TgJRHI

create a http notify.
[img1](https://github.com/andybrier/aliyun/blob/8e6f2e893cb5690a51a065f00e58e6ea77a150d2/oss/oss-to-s3/oss-setup-1.jpg)
[img2](https://github.com/andybrier/aliyun/blob/8e6f2e893cb5690a51a065f00e58e6ea77a150d2/oss/oss-to-s3/oss-setup-2.jpg)

# run the code 
- copy `app.py` to dir: `oss-to-s3`
- run: `python app.py`

