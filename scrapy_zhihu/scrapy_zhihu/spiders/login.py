# -*- coding: utf-8 -*-
import scrapy
import time
import hmac
from hashlib import sha1
import base64
import json
from scrapy_zhihu.items import *

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    headers = {
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/signup?next=%2F',
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
        'X-UDID': 'ADAvaN2zfA2PTtN3mvNvxiDRzfJE6K66GCI=',
        'X-Xsrftoken': '110bf7be-b63c-4812-980f-a6b41d1b5479'
    }

    headers_user = {
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/people/z-kqiang/following',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0',
        'x-udid': 'AHCrOyQhDw2PTlPxzSpov8Jpp_zmcbU4urs=',
        'Cookie': 'q_c1=8419dc5f80aa47838bfe84456299d627|1522544115000|1516278692000; _zap=30eed11c-f722-403b-be66-b74ee8d42a30; __utma=155987696.370231765.1524985036.1524985036.1525005340.2; __utmz=155987696.1524985036.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); d_c0="AHCrOyQhDw2PTlPxzSpov8Jpp_zmcbU4urs=|1517133620"; __DAYU_PP=vIzzmN2ImBAIJ7I7UR2B3686bbe435f8; l_cap_id="NWNjNWYzZGU4NDY3NDRjZDk5Mjk5Mjg2ZjdjYTJlZWU=|1524839735|05369c6a5212d668fad4b3f3a68bb1e2797c2618"; r_cap_id="Mzc3Njk4MmY2NTZmNDM5MmIzZGI0ZWIyY2ZmNGRkMGY=|1524839735|b806496afd89f5e4dedcf833c9a245307cd87e79"; cap_id="NWY2N2NlMjJmZjM1NGUwY2I1M2QyYjdhYjliOTQ2ODY=|1524839735|1b036fb2f2f0fd0d1690b692eaed90f225e654f8"; capsion_ticket="2|1:0|10:1525011467|14:capsion_ticket|44:YWVkNmM1MDgwOGQxNDNhNGI3ZGM3OWQ0NDg2OGE0MTA=|2b19d8dc4d249642d06a36006a453c6d76feff8466f8659232147c4852fa2014"; z_c0="2|1:0|10:1525011469|4:z_c0|92:Mi4xRnpLdEFnQUFBQUFBY0tzN0pDRVBEU1lBQUFCZ0FsVk5EU0xUV3dEWVpYWVN0Ri1UTWhaUEdnZDdYWkNZNmV6WktR|87fd77d2c64e8228910a1601470a3602d34cc1f7da84de69b90ef38e531cb9cf"; aliyungf_tc=AQAAAI6CUh3gOgkACiO4bnm6uuDh6oMA; _xsrf=aab27e4d-9839-4244-9448-7989c35dd8f0; __utmc=155987696'
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
        user = ZhihuUserItem()
        datas = json.loads(response.text)
        for i in range(len(datas['data'])):
            print(i)
            user['name'] = datas['data'][i]['name']
            if len(datas['data'][i]['badge']):
                user['description'] = datas['data'][i]['badge'][0]['description']
            else:
                user['description'] = ''
            user['url'] = datas['data'][i]['url']
            user['url_token'] = datas['data'][i]['url_token']
            user['follower_count'] = datas['data'][i]['follower_count']
            user['headline'] = datas['data'][i]['headline']
            user['type'] = datas['data'][i]['type']
            yield user

        for i in range(len(datas['data'])):
            url = 'https://www.zhihu.com/api/v4/members/{0}/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=0&limit=20'.format(datas['data'][i]['url_token'])
            yield scrapy.Request(url, headers=self.headers)



    def start_requests(self):
        """
        判断登录是否需要验证码
        :return:
        """
        yield scrapy.Request('https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
                             headers=self.headers, callback=self.is_need_captcha)

    def is_need_captcha(self, response):
        """
        根据返回结果判断登录是否需要验证码:
        需要，则去获得验证码;
        不需要，则直接向服务器发送表单数据，进行登录;
        :param response:
        :return:
        """
        #print(response.text)
        need_cap = json.loads(response.text)['show_captcha']

        # 获得验证码
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
            post_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
            post_data = {
                'client_id': self.client_id,
                'username': '+8618160013575',
                'password': 'w1234567',
                'grant_type': self.grant_type,
                'source': self.source,
                'timestamp': self.timestamp,
                'signature': self.get_signature(self.grant_type,
                                                self.client_id,
                                                self.source,
                                                self.timestamp
                                                ),
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
        """
        1.解析验证码，保存为图片，手动打码；
        2.发送包含验证码信息的表单数据给服务器，验证是否通过;
        :param response:
        :return:
        """
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
        """
        1.验证通过，发送包含表单信息给服务器，请求登录；
        2.验证不通过，返回输出；
        :param response:
        :return:
        """
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
            callback=self.start_crawl
        )

    def start_crawl(self, response):
        """
        随意选取一个用户的主页作为seed_url(关注人不为空)，开始收集知乎用户；
        :param response:
        :return:
        """
        print(response.status)
        yield scrapy.Request('https://www.zhihu.com/api/v4/members/zhou-bo-lei//followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=0&limit=20', headers=self.headers_user)



















