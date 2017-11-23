# encoding: utf-8
"""
@contact: lucky9322@163.com
@project: PYLesson
@software: PyCharm
@file: wyymusic_spider.py
@time: 2017/11/22 下午10:20

主要对网易云音乐的入住歌手(这里只处理了前60位)的粉丝进行了分析
1.歌手的受关注度（粉丝数量）
2.分析粉丝是否位僵尸粉（根据粉丝的动态）
3.粉丝的性别（得到歌手的受众群体）
4.粉丝的粉丝量（）
"""

import requests
from urllib import parse

url = 'http://music.163.com/discover/artist/signed/'
data = {
    'params': 'fJbo+HUI/8ybjgBmU+lS+cYKI8nlg8RlfLAUrLv3B28XEImnacTIViLdUTC2zhPfbDboYgH60deK0LQ2KaXiKFUvpFp6AIunoaPCP77caDlwvOJPV4566CpuT9Tvapt82AJYpitXzUj9vBqDSdI10q+BLBQg1bUQd5Lp28gCEmEIyyOX/V9ozShqUe0vFd7S',
    'encSecKey': 'b7e1ae5cc87affba4ae14dce2af836b64ae01824f71940c96c27c11b773c47d0d6fc2ead92266e6b6a01860c0c9c942b8e47929b026fa57a2198e3542183e5fd484b3b57c6493cc39a9b0621c39740a157302a713a8654bc1725eff7c5484548647f612e8b373abbf3b3a476fe2692202fc7a80986d84e3bbbe5f4169678528f'}
headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
response = requests.post(url, data, headers)
print(response.text)
