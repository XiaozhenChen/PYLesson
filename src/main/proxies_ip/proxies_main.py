# -*- coding: utf-8 -*-
# @Time    : 2017/11/29 上午10:57
# @Author  : zhangdongdong
# @Email   : lucky9322@163.com
# @File    : proxies_main.py
# @Software: PyCharm

'''
为requests设置代理

西刺免费代理ip
http://www.xicidaili.com/
快代理
http://www.kuaidaili.com/
代理66
http://www.66ip.cn/
guobanjia
http://www.goubanjia.com/free/gngn/index.shtml

查看当前ip
http://www.whatismyip.com.tw/
'''

from bs4 import BeautifulSoup
import requests


def get_current_ip():
    proxies = {
        "http": "223.223.203.30:8080"
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cookie': 'sc_is_visitor_unique=rx6392240.1511926158.9B55B6223BB64F94F9F8C096B8C957EC.1.1.1.1.1.1.1.1.1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Host': 'www.whatismyip.com.tw',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'}
    url = 'http://www.whatismyip.com.tw/'
    response = requests.get(url=url, headers=headers, proxies=proxies)
    if response.status_code == 200:
        bsObj = BeautifulSoup(response.content, 'html5lib')
        result = bsObj.find('span').find('b')
        print('当前的ip为====>', result.text)
    else:
        print(response.status_code)


def main():
    get_current_ip()


if __name__ == '__main__':
    main()
