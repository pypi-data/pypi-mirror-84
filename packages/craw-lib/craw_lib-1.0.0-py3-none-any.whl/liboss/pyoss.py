#!/usr/bin/python
#coding:utf-8
import os
import oss2
# 以下代码展示了文件下载的用法，如下载文件、范围下载、断点续传下载等。
#https://github.com/aliyun/aliyun-oss-python-sdk/blob/master/examples/download.py
# 首先初始化AccessKeyId、AccessKeySecret、Endpoint等信息。
# 通过环境变量获取，或者把诸如“<你的AccessKeyId>”替换成真实的AccessKeyId等。
#
# 以杭州区域为例，Endpoint可以是：
#   http://oss-cn-hangzhou.aliyuncs.com
#   https://oss-cn-hangzhou.aliyuncs.com
# 分别以HTTP、HTTPS协议访问。
class pyOss:
	def __init__(self):
		access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', '')
		access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', '')
		bucket_name = os.getenv('OSS_TEST_BUCKET', '')
		endpoint = os.getenv('OSS_TEST_ENDPOINT', '')
		self.bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

	def upload(self,remote_file,local_file):
		self.bucket.put_object_from_file(remote_file, local_file)