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

import base64
import json
from Crypto.Cipher import AES
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

first_param = "{rid:\"\", offset:\"0\", total:\"true\", limit:\"20\", csrf_token:\"\"}"
forth_param = "0CoJUm6Qyw8W8jud"


def get_params():
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText


# 获取 encSecKey
def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


# 解密过程
def AES_encrypt(text, key, iv):
    # print('======',type(text))
    pad = 16 - len(text) % 16
    if type(text) == str:
        text = text + pad * chr(pad)
    else:
        text = text.decode() + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    # print(text,len(text))
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text


headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
           'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate',
           'Cookie': '_ntes_nuid=904d3b8b89420e70860b83bf75fab2bf; vjuids=b0c43dff2.15df4be65bb.0.469bb6bd80ac5; vjlast=1503049705.1503049705.30; _ntes_nnid=1c55be8f4d29b4fb173c112779e77a1e,1503049704906; vinfo_n_f_l_n3=8a108ed17f5e2bee.1.0.1503049704933.0.1503049735524; usertrack=c+xxClmeM+l4La3LCGqbAg==; mail_psc_fingerprint=a3609f4385a6bb0b81e2ca682ca84143; Qs_lvt_73318=1509587605; Qs_pv_73318=1033010771750290600%2C3172801563243570000%2C2089498687280593000%2C4157715173816772600; __utma=187553192.700510131.1503540205.1504103232.1510391470.2; __utmz=187553192.1504103232.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __oc_uuid=4fa6ca20-8d8f-11e7-88e3-4d048af0b908; _ga=GA1.2.700510131.1503540205; __q_=1; P_INFO=13522813097|1511505778|0|kaola|00&99|null&null&null#zhj&330100#10#0#0|&0||13522813097; NTES_YD_PASSPORT=_59QDZOCX69182EAbuBtJkONsAQrnOQHfNtYlaF0p7psQkujQqfOaE88p.TKSo9x5RnQOiWUkP5GyOq6LeXT4wQePLDkyxYv4ObZrELlXzbF9fGQJLG00Mk2pejdK0ABnQXoW2A9L84sE; KAOLA_ACC=yd.ebe8d228456c4a3d9@163.com; JSESSIONID-WYYY=rznp%5CxyHfCvxiTBJq6KQ5Rh05uqUj5RiIf%5CYIqkMvvBQGbWE3tdH8nWRaV%5CdOq3n3deuGHO4M8kzCN%2ByFSQNOT%2B1smEfkoSH%2BpGocIhhjsqr01eUnBrzZQd2%5COUR6WKrii1CZr9Ahb75OAp4nZjTmzp4GODXZ5UriOmna%2Bq%5CWWm5nWQ4%3A1511700110176; _iuqxldmzr_=32; __utma=94650624.700510131.1503540205.1511665674.1511699054.22; __utmb=94650624.11.10.1511699054; __utmc=94650624; __utmz=94650624.1509098083.8.7.utmcsr=monkeyblog.cn|utmccn=(referral)|utmcmd=referral|utmcct=/',
           'Connection': 'keep-alive',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Host': 'music.163.com',
           'Origin': 'http://music.163.com',
           'Referer': 'http://music.163.com/discover/artist/signed/'
           }


def get_raw_artist():
    try:
        url = 'http://music.163.com/weapi/artist/list?csrf_token='
        data = {
            'params': get_params(),
            'encSecKey': get_encSecKey()
        }
        response = requests.post(url=url, data=data, headers=headers)
        if response.status_code == 200:
            if len(response.content):
                return response.content
            return get_raw_artist()
        return None
    except HTTPError as e:
        print('获取歌手列表失败', e)
        return None


def get_artist(rawData):
    if rawData:
        jsonObj = json.loads(rawData.decode('utf-8'))
        for item in jsonObj['artists']:
            yield {
                'img': item['img1v1Url'],
                'id': item['id'],
                'name': item['name']
            }
    else:
        print('暂时没有获取到入住歌手列表')


def main():
    rawData = get_raw_artist()
    print(rawData)
    for item in get_artist(rawData):
        print(item)


if __name__ == '__main__':
    main()
