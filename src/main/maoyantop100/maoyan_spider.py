# encoding: utf-8
"""
@contact: lucky9322@163.com
@project: PYLesson
@software: PyCharm
@file: maoyan_spider.py
@time: 2017/11/23 下午2:51
"""
import json
import re
import requests
from requests.exceptions import RequestException
from multiprocessing import Pool


def get_one_page(url):
    try:
        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        print('获取页面失败', e)
        return None


def parse_one_page(html):
    pattern = re.compile(
        r'<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?"star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',
        re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }


def write_to_file(content):
    # a模式 追加模式
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    rawHtml = get_one_page(url)
    # print(rawHtml)
    for item in parse_one_page(rawHtml):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    # main()
    # for i in range(10):
    #     main(i * 10)
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])
