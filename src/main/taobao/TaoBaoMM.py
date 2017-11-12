# encoding: utf-8
"""
@contact: lucky9322@163.com
@project: PYLesson
@software: PyCharm
@file: TaoBaoMM.py
@time: 2017/11/12 下午5:59
"""

'''
1.抓取淘宝MM的姓名，头像，年龄
'''
from urllib.request import urlopen
from urllib.error import HTTPError
import re
import os
from src.main.util.Tool import Tool


class Spider(object):
    # 页面初始化
    def __init__(self):
        self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
        self.tool = Tool()

    # 获取索引页面的内容
    def getPage(self, pageIndex):
        try:
            url = self.siteURL + '?page=' + str(pageIndex)
            response = urlopen(url)
            # print(response.read().decode('gbk'))
            return response.read().decode('gbk')
        except HTTPError as e:
            print(e.reason)
            return None

    # 获取索引界面所有MM的信息，list格式
    def getContents(self, pageIndex):
        rawPage = self.getPage(pageIndex)
        # <div class="list-item.*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>
        pattern = re.compile(
            r'<div class="list-item.*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',
            re.S)
        items = re.findall(pattern, rawPage)
        contents = []
        for item in items:
            # print(item[0], item[1], item[2], item[3], item[4])
            contents.append(('http:'+item[0], 'http:'+item[1], item[2], item[3], item[4]))
        return contents

    def getDetailPage(self, infoRul):
        try:
            response = urlopen(infoRul)
            return response.read().decode('gbk')
        except HTTPError as e:
            print(e.reason)
            return None

    # 获取个人文字简介
    def getBrief(self, page):
        pattern = re.compile(r'<div class="mm-aixiu-content".*?>(.*?)<!--', re.S)
        result = re.search(pattern, page)
        return self.tool.replace(result.group(1))

    def getAllImg(self, page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--', re.S)
        # 个人信息页面所有代码
        content = re.search(pattern, page)
        # 从代码中提取图片
        patternImg = re.compile('<img.*?src="(.*?)"', re.S)
        images = re.findall(patternImg, content.group(1))
        return images

    # 保存多张写真照片
    def saveImgs(self, images, name):
        number = 1
        print('发现', name, '共有', len(images), '张照片')
        for imageUrl in images:
            splitPath = imageUrl.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = 'jpg'
            fileName = name + "/" + str(number) + "." + fTail
            self.saveImg("http:"+imageUrl, fileName)
            number += 1

    # 保存头像
    def saveIcon(self, iconUrl, name):
        splitPath = iconUrl.split('.')
        fTail = splitPath.pop()
        if len(fTail) > 3:
            fTail = 'jpg'
        fileName = name + '/icon.' + fTail
        self.saveImg(iconUrl, fileName)

    # 传入图片地址，文件名，保存单张图片
    def saveImg(self, imageUrl, fileName):
        response = urlopen(imageUrl)
        data = response.read()
        f = open(fileName, 'wb')
        f.write(data)
        print("正在悄悄保存她的一张图片为", fileName)
        f.close()

    # 写入文本
    def saveBrief(self, content, name):
        fileName = name + '/' + name + '.txt'
        f = open(fileName, 'w+')
        f.write(content)
        print('正在偷偷保存她的信息为：' + fileName)
        f.close()

    # 创建新目录
    def makeDir(self, path):
        path = path.strip()
        # 判断路径是否存在
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            return False

    def savePageInfo(self, pageIndex):
        # 获取第一页淘宝MM列表
        contents = self.getContents(pageIndex)
        for item in contents:
            # item[0]个人详情URL,item[1]头像URL,item[2]姓名,item[3]年龄,item[4]居住地
            print("发现一位模特,名字叫", item[2], u"芳龄", item[3], u",她在", item[4])
            print("正在偷偷地保存", item[2], "的信息")
            print("又意外地发现她的个人地址是", item[0])
            # 个人详情页面的URL
            detailURL = item[0]
            #             得到个人详情页代码
            detailPage = self.getDetailPage(detailURL)
            # 获取个人简介
            brief = self.getBrief(detailPage)
            #             获取所有图片列表
            imgs = self.getAllImg(detailPage)
            self.makeDir(item[2])
            # 保存个人简介
            self.saveBrief(brief, item[2])
            # 保存头像
            self.saveIcon(item[1], item[2])
            self.saveImgs(imgs, item[2])

    def savePagesInfo(self, start, end):
        for i in range(start, end):
            print("正在偷偷寻找第", i, "个地方，看看MM们在不在")
            self.savePageInfo(i)


# 传入起止页码即可，在此传入了2,10,表示抓取第2到10页的MM
spider = Spider()
# spider.savePagesInfo(2, 10)
spider.savePageInfo(2)
