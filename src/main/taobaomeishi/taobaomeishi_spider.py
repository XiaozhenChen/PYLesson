# encoding: utf-8
"""
@contact: lucky9322@163.com
@project: PYLesson
@software: PyCharm
@file: taobaomeishi_spider.py
@time: 2017/11/24 上午11:45
"""
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from pyquery import PyQuery as pq


# brower = webdriver.Chrome('/Users/lucky/Downloads/chromedriver/chromedriver')
brower = webdriver.PhantomJS('/Users/lucky/Downloads/phantomjs/bin/phantomjs')

wait = WebDriverWait(brower, 10)

brower.set_window_size(1400,900)

def search():
    try:
        brower.get('https://www.taobao.com/')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        # 搜索按钮查找时，报超时，该用模拟回车
        # summit = wait.until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_SearchForm > button"))
        # )
        input.send_keys('美食')
        input.send_keys(Keys.ENTER)
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        parse_product()
        return total.text
    except WebDriverException as e:
        print('搜索异常', e)
        return search()


def next_page(page_number):
    try:
        inpuT = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input')))
        summit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        inpuT.clear()
        inpuT.send_keys(page_number)
        summit.click()
        print('当前页', page_number)
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))

        parse_product()
    except WebDriverException as e:
        print('下一页异常', page_number, e)
        next_page(page_number)


def parse_product():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = brower.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        # print(item)
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)


def main():
    try:
        total = search()
        total = int(re.compile(r'(\d+)').search(total).group(1))
        # print(total)
        for i in range(2, total + 1):
            next_page(i)
            # print(i)
    finally:
        brower.close()


if __name__ == '__main__':
    main()
