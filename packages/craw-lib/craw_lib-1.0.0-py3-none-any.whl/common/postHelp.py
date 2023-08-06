#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

PY2 = sys.version_info[0] == 2
if PY2:
    import urllib
    import urllib2
else:
    import urllib.request as urllib2
    import urllib.parse as urllib

if sys.platform == 'linux':
    sys.path.append('/home/deploy/bbs-fetch/lib')
else:
    sys.path.append('/Users/momo/PycharmProjects/bbs-fetch/lib')
from common.ipHelp import IpProxy


def sendpost(url, headers, values):
    postdata = urllib.urlencode(values).encode('utf8')  # 进行编码
    request = urllib2.Request(url, headers=headers, data=postdata)
    response = urllib2.urlopen(request).read()
    return response


def requestsGet(url, headers, ip_proxy, cookies, source):
    try:
        if headers:
            if ip_proxy and cookies:
                res = requests.get(url, headers=headers, proxies=ip_proxy, cookies=cookies, timeout=(5, 10))
            elif ip_proxy:
                res = requests.get(url, headers=headers, proxies=ip_proxy, timeout=(5, 10))
            elif cookies:
                res = requests.get(url, headers=headers, cookies=cookies, timeout=(5, 10))
            else:
                res = requests.get(url, headers=headers, timeout=(5, 10))
        else:
            if ip_proxy and cookies:
                res = requests.get(url, proxies=ip_proxy, cookies=cookies, timeout=(5, 10))
            elif ip_proxy:
                res = requests.get(url, proxies=ip_proxy, timeout=(5, 10))
            elif cookies:
                res = requests.get(url, cookies=cookies, timeout=(5, 10))
            else:
                res = requests.get(url, timeout=(5, 10))
        if res.status_code == 200:
            return res
        else:
            print('状态码错误:' + str(res.status_code) + url)
            return ''
    except requests.exceptions.InvalidProxyURL:
        print(source + ' 代理获取失败')
        return ''
    except requests.exceptions.TooManyRedirects:
        print(source + ' ip被封')
        return ''
    except requests.RequestException as e:
        print(e)
        return ''


def browserSoup(url):  # htmlText = soup.prettify(formatter="html")
    # 通过模拟浏览器请求数据
    chrome_options = Options()
    chrome_options.add_argument("headless")
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    # proxy = IpProxy()
    # ip_proxy = proxy.getIpProxy('http', True)
    # print(ip_proxy)
    # chrome_options.add_argument('--proxy-server=http://{0}'.format(ip_proxy))
    chrome_options.add_argument(
        'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/78.0.3904.70 Safari/537.36"')
    if sys.platform == 'linux':
        executable_path = '/home/deploy/bbs-fetch/chromedriver'
    else:
        executable_path = '/Users/hykfft/codes/chromedriver'
    browser = webdriver.Chrome(
        executable_path=executable_path,
        chrome_options=chrome_options
    )
    browser.get(url)
    response = browser.page_source
    browser.quit()
    soup = BeautifulSoup(response, "html.parser")
    [s.extract() for s in soup("script")]
    [s.extract() for s in soup("style")]
    [s.extract() for s in soup("meta")]
    [s.extract() for s in soup("link")]
    return soup


def get_soup(resp):
    return BeautifulSoup(resp.text, "html.parser")


'''
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page,fromEncoding="utf-8")
    print soup.originalEncoding
这行代码来确定乱码所用的编码方式是什么。
'''
