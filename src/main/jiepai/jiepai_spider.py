# encoding: utf-8
"""
@contact: lucky9322@163.com
@project: PYLesson
@software: PyCharm
@file: jiepai_spider.py
@time: 2017/11/21 上午11:07
"""
import json
from urllib.parse import urlencode
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re

import requests
import os
from hashlib import md5
from multiprocessing import Pool
from json.decoder import JSONDecodeError
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='scraping')


def get_page_index(offset, keyword):
    data = {'offset': offset,
            'format': 'json',
            'keyword': keyword,
            'autoload': 'true',
            'count': 20,
            'cur_tab': 3}
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as  e:
        print('请求索引页失败')
        return None


def parse_page_index(html):
    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass


def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错', url)
        return None


def parse_page_detail(html, url):
    bsObj = BeautifulSoup(html, 'html5lib')
    title = bsObj.select('title')[0].get_text()
    print(title)
    images_pattern = re.compile(r'gallery: JSON.parse\("(.*?)"\),', re.S)
    result = re.search(images_pattern, html)
    if result:
        # print(result.group(1))
        pattern = re.compile(r'\\')
        tmp = re.sub(pattern, '', str(result.group(1)))
        data = json.loads(tmp)
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:
                download_image(image)
            return {'title': title,
                    'url': url,
                    'images': images
                    }


def save_to_mysql(data):
    pass
    # try:
    #     cursor = conn.cursor()
    #     insert_sql = "insert into"
    #     cursor.execute(insert_sql)
    #     conn.commit()
    # except Exception as e:
    #     conn.rollback()
    #     print('保存数据库异常', e)
    # finally:
    #     conn.close()


def download_image(url):
    print('正在下载', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print('下载图片失败', url)
        return None


def save_image(content):
    # 路径，文件名，后缀
    file_path = '{0}/{1}.{2}'.format(os.getcwd() + '/res', md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def main(offset):
    rawHtml = get_page_index(offset, '街拍')
    for url in parse_page_index(rawHtml):
        detailHtml = get_page_detail(url)
        if detailHtml:
            result = parse_page_detail(detailHtml, url)
            print(result)
            if result:
                save_to_mysql(result)


if __name__ == "__main__":
    main()
    print(os.getcwd())
    groups = [x * 20 for x in range(0, 20 + 1)]
    pool = Pool()
    pool.map(main, groups)
