# -*- coding:utf-8 -*-
"""
点击爱奇艺视频的分享按键，复制flash地址，
例如http://player.video.qiyi.com/232c93cafe55a62e05877eb7bac1e6ab/0/0/v_19rrchb25s.swf-albumId=982439900-tvId=982439900-isPurchase=0-cnId=6，
分析该地址后得到模板为http://player.video.qiyi.com/xxx/0/0/xxx.swf-albumId=xxx-tvId=xxx-isPurchase=0-cnId=6，而xxx所代表的参数在html中均可以找到
"""

import lxml.html
import requests
import urllib.request
import cssselect
import random
import re
import urllib.parse


def iqiyi_crawler(retries, user_agent, url):
    """

    :param retries:
    :param user_agent:
    :param url:
    :return:
    """
    header = {
        "Host": "www.iqiyi.comm",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": 'no-cache',
        "Connection": "keep-alive",
        "User-Agent": user_agent
    }
    try:
        #req = urllib.request.Request(url, headers=header, method='POST')
        html = urllib.request.urlopen(url).read().decode()
    except urllib.request.URLError as e:
        print('error reason is ', e.reason)
        html = None

        if retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                iqiyi_crawler(retries - 1, user_agent, url)
    return html


def get_paras_from_html(html, url):
    """
    需抽取的数据为：
    param['vid']，
    param['albumId']，
    param['tvid']，
    和url中的xxx.html

    :param url:
    :param html:
    :return:
    """
    param = {}
    if html:
        tree = lxml.html.fromstring(html)
        td = tree.cssselect('div#block-B.videoArea > div#flashbox > script')[0].text_content()
        # 选出数据块，然后对数据块进行加工整理，得到字典格式
        list = [x.strip() for x in td.split(';')]

        list.pop(0)  # 删除无用数据
        list.pop(0)
        list.pop()
        list.pop()

        # exec真强大！
        for x in list[:6]:
            exec(x)

        # 抽取url中的path
        path = urllib.parse.urlparse(url).path.split('.')[0]
    else:
        param['vid'] = None
        param['albumId'] = None
        param['tvid'] = None
        path = None

    return param['vid'], param['albumId'], param['tvid'], path


if __name__ == '__main__':
    url = 'http://www.iqiyi.com/v_19rrcaoes0.html'  # 随意一个视频网页地址

    # 随机获取一个user_agent，反爬
    with open('/home/wangf/PycharmProjects/spiders/user_agent.txt', 'r') as fp:
        user_agents = fp.readlines()
    user_agents = list(map(lambda x: x.strip(), user_agents))  # 去除每行的换行符
    uagent = random.choice(user_agents)

    h = iqiyi_crawler(3, uagent, url)
    vid, albumId, tvid, path = get_paras_from_html(h, url)

    print('http://player.video.qiyi.com/%s/0/0%s.swf-albumId=%s-tvId=%s-isPurchase=0-cnId=6'%(vid,path,albumId,tvid))
