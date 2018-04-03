# -*- coding:utf-8 -*-

"""
爬取优酷视频的地址
"""

import requests
import re
import random


def down_loader(retries, user_agent, url):
    """

    :param retries: 重试次数
    :param url: seed_url
    :return: html
    """
    header = {
        'Host': "v.youku.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        'Cache-Control': 'no-cache',
        "Connection": "keep-alive",
        "User-Agent": user_agent,
        'Referer': 'http://www.youku.com/'
    }

    try:
        html = requests.get(url, headers=header).text
    except urllib.request.URLError as e:
        print('error reason is ', e.reason)
        html = None

        # 当返回http码为4xx时表示发生请求端错误, 5xx时表示发生服务器错误, 这种情况下可重试
        if retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                down_loader(retries - 1, user_agent, url)
    return html


if __name__ == '__main__':
    # 随机找一个优酷视频网址
    seed_url = 'http://v.youku.com/v_show/id_XMzQ4MzM0MDY2MA==.html?spm=a2h0j.11185381.listitem_' \
               'page1.5!2~A&s=da8f44281aefbfbd11ef'

    with open('/home/wangf/PycharmProjects/spiders/user_agent.txt', 'r') as fp:
        user_agents = fp.readlines()
    user_agents = list(map(lambda x: x.strip(), user_agents))  # 去除每行的换行符

    user_agent = random.choice(user_agents)

    html = down_loader(3, user_agent, seed_url)

    if html:
        urls = re.findall('<embed src=\'(.*?)\'', html)
    print(urls)

#  -------------------测试结果-------------------------------
#  将此链接放在浏览器中可以直接播放
#  [
#  u'http://player.youku.com/player.php/sid/XMTgzNDI0MjkzNg==/v.swf',
#  u'http://player.youku.com/player.php/sid/XMTgzNDI0MjkzNg==/v.swf'
#  ]
