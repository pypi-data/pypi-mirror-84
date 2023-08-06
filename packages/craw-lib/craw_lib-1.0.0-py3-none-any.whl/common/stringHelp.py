#!/usr/bin/python
# coding:utf-8
import json
import random
import re
import requests
import string
import sys
from collections import Counter

import jieba
import jieba.analyse as analyse
from gne import GeneralNewsExtractor

sys.path.append('/Users/momo/PycharmProjects/bbs-fetch/lib')
from common.ipHelp import IpProxy

PY2 = sys.version_info[0] == 2
'''
就是Python2中的str在Python3中为bytes，Python 2中的unicode是Python 3中的str。

问题出在python3.5和Python2.7在套接字返回值解码上有区别:
python bytes和str两种类型可以通过函数encode()和decode()相互转换，
str→bytes：encode()方法。str通过encode()方法可以转换为bytes。
bytes→str：decode()方法。如果我们从网络或磁盘上读取了字节流，那么读到的数据就是bytes。
要把bytes变为str，就需要用decode()方法。
'''
proxy = IpProxy()
extractor = GeneralNewsExtractor()


# python3中为string.ascii_letters,而python2下则可以使用string.letters和string.ascii_letters
def genWord(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.sample(chars, length))  # 得出的结果中字符不会有重复的


# 判断字符串是否包含字符串
def contains():
    site = '判断字符串是否包含字符串'
    if "包含" in site:  # 方法一
        print('site contains')

    if site.find("包含") == -1:  # 方法二
        print('site contains')


# 截取字符串
def block():
    s = '去sxs年这个时候，我在敦煌的蚂蚁森林种下了梭梭树，当时我们说，2020年我们要再种下1亿棵树！这个2020年来得很特殊'
    # s = s.decode('utf8')[0:10].encode('utf8')
    s = s[0:10]
    print(s)


# json格式化输出
def jsonPrint(response):
    jsonString = json.dumps(response, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))
    print(jsonString)


def byteify(data, ignore_dicts=False):  # 写入文件时格式化数据
    # if this is a unicode string, return its string representation
    if PY2:
        if isinstance(data, unicode):
            return data.encode('utf-8')
    else:
        if isinstance(data, str):
            return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [byteify(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return dict(
            (byteify(key, ignore_dicts=True), byteify(value, ignore_dicts=True)) for key, value in data.iteritems())
    # if it's anything else, return it in its original form
    return data


def jiebaCut(pageInfo):
    word_list = []
    wordLists = []
    value_cut = jieba.cut(pageInfo)
    value_cut = [w for w in value_cut if len(w) > 1]
    stopWords = ['我们', '这个', '不是', '一个', '一些', '每个', '每天', '可以']
    value_cut = [w for w in value_cut if w not in stopWords]
    for cut in value_cut:
        word_list.append(cut)
    result = dict(Counter(word_list))
    sorted_bow = sorted(result.items(), key=lambda d: d[1], reverse=True)
    for (k, v) in sorted_bow[:10]:
        word = "%s-%d" % (k, v)
        wordLists.append(word)
    frequency = ','.join(wordLists)
    return frequency


def extractPageInfo(pageUrl):
    """
    获取文章详情
    :param pageUrl:
    :param pageId:
    :return:
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/55.0.2883.95 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
    ip_proxy = proxy.getIpProxy('http')
    response = requests.get(pageUrl, headers=headers, proxies=ip_proxy)
    result = extractor.extract(response.text)
    images = result['images']  # 文章里的图片
    content = result['content']
    frequency_arr = analyse.extract_tags(result['content'], topK=10, withWeight=True, allowPOS=())
    tags = []
    for (k, v) in frequency_arr:
        tags.append(k)
    return images, content, tags


def extractTextHtml(htmlText):
    htmlText = '<html><body>' + htmlText + '</body></html>'
    result = extractor.extract(htmlText)
    images = result['images']  # 文章里的图片
    content = result['content']
    frequency_arr = analyse.extract_tags(result['content'], topK=10, withWeight=True, allowPOS=())
    tags = []
    for (k, v) in frequency_arr:
        tags.append(k)
    return images, content, tags


def emojiReplace(content, relpaceStr):  # python3 通过
    try:
        myre = re.compile(u'['u'\U0001F300-\U0001F64F'u'\U0001F680-\U0001F6FF'u'\u2600-\u2B55'u'\u20e3'u'\ufe0f]+', re.UNICODE)
    except re.error:
        myre = re.compile(u'('u'\ud83c[\udf00-\udfff]|'u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'u'[\u2600-\u2B55])+', re.UNICODE)
    return myre.sub(relpaceStr, content)


def gen_num_str(str_len=10):
    return ''.join(['%s' % random.randint(0, 9) for num in range(0, str_len)])
