# -*- coding:utf-8 -*-

import requests

url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
headers = {
    'accept': 'application/json, text/plain, */*',
    'Accept-Lanuage': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Mobile Safari/537.36',
    'Referer': 'https://www.zhihu.com/signin?next=https%3A%2F%2Fwww.zhihu.com%2F',
}

class ZhihuSigninSpider(self):
    def __init__(self):
        pass