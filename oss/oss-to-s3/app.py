# -*- coding: utf-8 -*-
# doc: https://help.aliyun.com/document_detail/122379.html?spm=a2c4g.11174283.6.837.32847da2TgJRHI

from flask import Flask
app = Flask(__name__)

@app.route('/oss/notify')
def oss_notify():
   return 'Hello World’

if __name__ == '__main__':
   app.run()