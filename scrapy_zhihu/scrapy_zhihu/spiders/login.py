# -*- coding: utf-8 -*-
import scrapy
import time
import hmac
from hashlib import sha1
import base64
import json

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['zhihu.com']
    # start_urls = ['https://www.zhihu.com/signin']
    start_urls = ['https://www.zhihu.com/']
    agent = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; GoogleT5)'
    headers = {
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/signup?next=%2F',
        'User-Agent': agent,
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
        #'X-UDID': 'ADAvaN2zfA2PTtN3mvNvxiDRzfJE6K66GCI=',
        #'X-Xsrftoken': '110bf7be-b63c-4812-980f-a6b41d1b5479'
    }

    grant_type = 'password'
    client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
    source = 'com.zhihu.web'
    timestamp = str(int(time.time()*1000))

    def get_signature(self, grant_type, client_id, source, timestamp):
        hm = hmac.new(b'd1b964811afb40118a12068ff74a12f4', None, sha1)
        hm.update(str.encode(grant_type))
        hm.update(str.encode(client_id))
        hm.update(str.encode(source))
        hm.update(str.encode(timestamp))
        return str(hm.hexdigest())

    def parse(self, response):
        print(response.body.decode('utf-8'))

    def is_need_captcha(self, response):
        print(response.text)
        need_cap = json.loads(response.body)['show_captcha']
        print(need_cap)

        if need_cap:
            print('captcha is needed')
            yield scrapy.Request(
                url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
                headers=self.headers,
                callback=self.captcha,
                method='PUT'
            )
        else:
            print('captcha is not needed')
            post_url = 'https://www.zhihu.com/api/v3/oauth/signin'
            post_data = {
                'client_id': self.client_id,
                'username': '18160013575',
                'password': 'w1234567',
                'grant_type': self.grant_type,
                'source': self.source,
                'timestamp': self.timestamp,
                'signature': self.get_signature(self.grant_type,
                                                self.client_id,self.timestamp),
                'lang': 'en',
                'ref_source': 'homepage',
                'captcha': '',
                'utm_source': ''
            }
            yield scrapy.FormRequest(
                url=post_url,
                formdata=post_data,
                headers=self.headers,
                callback=self.check_login
            )

    def captcha(self, response):
        #print(response.body)
        try:
            img = json.loads(response.body)['img_base64']
        except ValueError:
            print('get img_base64 failed')
        else:
            img = img.encode('utf8')
            img_data = base64.b64decode(img)

            with open('zhihu.gif', 'wb') as f:
                f.write(img_data)
                f.close()
        captcha = input('input captcha: ')
        post_data = {
            'input_text': captcha
        }
        yield scrapy.FormRequest(
            url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
            formdata=post_data,
            callback=self.captcha_login,
            headers=self.headers
        )

    def captcha_login(self, response):
        try:
            cap_result = json.loads(response.body)['success']
            print(cap_result)
        except ValueError:
            print('关于验证码的POST请求响应失败')
        else:
            if cap_result:
                print('验证成功')
        post_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        post_data = {
            'client_id': self.client_id,
            'username': '18160013575',
            'password': 'w1234567',
            'grant_type': self.grant_type,
            'source': self.source,
            'timestamp': self.timestamp,
            'signature': self.get_signature(self.grant_type,
                                            self.client_id, self.timestamp),
            'lang': 'en',
            'ref_source': 'homepage',
            'captcha': '',
            'utm_source': ''
        }
        headers = self.headers
        headers.update({
            'Origin': 'https://www.zhihu.com',
            'Pragma': 'no - cache',
            'Cache-Control': 'no - cache'
        })
        yield scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=headers,
            callback=self.check_login
        )

    def check_login(self, response):
        text_json = json.loads(response.text)
        print(text_json)
        yield scrapy.Request('https://www.zhihu.com/inbox', headers=self.headers)



















