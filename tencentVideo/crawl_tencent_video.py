# -*- coding:utf-8 -*-

"""
腾讯视频所用技术时常更新，百度的网友方法都不适用，所以自己探索新的规律:
使用每个视频的分享功能，复制html代码，从中抽取视频的url，发现规律为
https://imgcache.qq.com/tencentvideo_v1/playerv3/TPout.swf?max_age=86400&v=20161117&vid=xxx&auto=0，
所以只需要找到每个视频vid，就算爬取到了视频
"""

import requests
import re
import random


def tencent_crawler(retries, user_agent, url):
    """
    :param retries:
    :param user_agent:
    :param url: 视频所在网页地址
    :return:html of the url
    """
    header = {
        'Host': "v.qq.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        'Cache-Control': 'no-cache',
        "Connection": "keep-alive",
        "User-Agent": user_agent,
        'Referer': 'https://v.qq.com/'
    }

    try:
        html = requests.get(url, headers=header, timeout=30).text
    except urllib.request.URLError as e:
        print('error reason is ', e.reason)
        html = None

        # 当返回http码为4xx时表示发生请求端错误, 5xx时表示发生服务器错误, 这种情况下可重试
        if retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                down_loader(retries - 1, user_agent, url)
    return html


def get_vid_from_html(html):
    """

    :param html: html
    :return: vid
    """
    # vid = re.findall('&vid=(.*?)&', html)
    vid = re.findall('&vid=(.*?)&', html)
    return vid


if __name__ == '__main__':
    url = 'https://v.qq.com/x/cover/1egcxh1l6d8jyt1/l0026d2zdci.html'  # 随意一个视频网页地址

    # 随机获取一个user_agent，反爬
    with open('/home/wangf/PycharmProjects/spiders/user_agent.txt', 'r') as fp:
        user_agents = fp.readlines()
    user_agents = list(map(lambda x: x.strip(), user_agents))  # 去除每行的换行符
    uagent = random.choice(user_agents)

    h = tencent_crawler(3, uagent, url)
    vid = get_vid_from_html(h)
    print('https://imgcache.qq.com/tencentvideo_v1/playerv3/TPout.swf?max_age=86400&v=20161117&vid=%s&auto=0' % vid[0])

#  -------------------测试结果-------------------------------
#  将此链接放在火狐浏览器中可以直接播放,但是chrome有时候不行
#  https://imgcache.qq.com/tencentvideo_v1/playerv3/TPout.swf?max_age=86400&v=20161117&vid=l0026d2zdci&auto=0,
