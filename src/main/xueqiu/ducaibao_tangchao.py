# encoding: utf-8
"""
Project: PYLesson
File: ducaibao_tangchao.py
Created by Zdd on 2018/1/25.

获取雪球 大v 唐朝 分享 "手把手教你读财报" 目录及 对应文章
将其 转成pdf 便于查看
"""

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import pdfkit

headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

def getPageList():
    try:
        url = 'https://xueqiu.com/8290096439/30887463'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content
        return None
    except RequestException as e:
        print()


def parseList(rawHtml):
    detailList = []
    bsObj = BeautifulSoup(rawHtml, 'html5lib')
    articleList = bsObj.find('div', {'class': 'article__bd__detail'})
    # print(articleList)
    linkList = articleList.find_all('a')
    i = 0
    for link in linkList:
        print(link['href'])
        writeToPdf(link['href'], str(i) + '.pdf')
        i = i + 1


def writeToPdf(url,name):
    path_wkhtmltopdf = r'/usr/local/bin/wkhtmltopdf'
    pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_url(url, name)


if __name__ == '__main__':
    rawHtml = getPageList()
    parseList(rawHtml)
