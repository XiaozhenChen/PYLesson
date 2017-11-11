# encoding: utf-8
"""
@contact: lucky9322@163.com
@project: PYLesson
@software: PyCharm
@file: BaiDuTieBa.py
@time: 2017/11/11 下午5:20
"""
'''
抓取百度贴吧帖子
1.对百度贴吧任意帖子进行抓取
2.指定是否只抓取楼主内容
3.将住区的内容分析并保存文件
'''

from urllib.request import urlopen
from urllib.error import HTTPError
import re
from src.main.util.Tool import Tool


class BDTB(object):
    # 初始化，传入基地址，是否只看楼主参数
    def __init__(self, baseUrl, seeLZ, floorTag):
        # base 链接地址
        self.baseURL = baseUrl
        # 是否只看楼主
        self.seeLZ = "?see_lz=" + str(seeLZ)
        # html 标签剔除工具类对象
        self.tool = Tool()
        #     全局file对象，文件写入操作对象
        self.file = None
        # 楼层标号，初始为1
        self.floor = 1
        # 默认的标题，如果没有成功获取到标题的话则会用这个标题
        self.defaultTitle = u'百度贴吧'
        # 是否写入楼分隔符的标记
        self.floorTag = floorTag

    # 传入页码，获取该页帖子的代码
    def getPage(self, pageNum):
        try:
            response = urlopen(self.baseURL + '?pn=' + str(pageNum))
            # 返回UTF-8格式编码内容
            return response.read().decode('utf-8')
        except HTTPError as e:
            print(e.reason)
            return None

    # 获取帖子标题
    def getTitle(self, rawPage):
        # 将正则表达式编译成pattern对象
        # <h3 class="core_title_txt pull-left text-overflow
        pattern = re.compile(r'<h3 class="core_title_txt pull-left text-overflow.*?>(.*?)</h3>', re.S)
        result = re.search(pattern, rawPage)
        if result:
            # print(result.group(1).strip())
            return result.group(1).strip()
        else:
            return None

    def getPageNum(self, rawPage):
        # print(rawPage)
        #         编译正则表达式，得到pattern对象
        #         <span class="red" >36</span>
        pattern = re.compile(r'<span class="red">([0-9]*)</span>', re.S)
        result = re.search(pattern, rawPage)
        if result:
            # print(result.group(1).strip())
            return result.group(1)
        else:
            return None

    # 获取每一层楼的内容，传入内容
    def getContent(self, page):
        pattern = re.compile(r'<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        floor = 1
        contents = []
        for item in items:
            #             print(
            #                 str(
            #                     floor) + '楼 ---------------\
            # ----------------\
            # ----------------\
            # ----------------\
            # ----------------\
            # ----------------\
            # ----------------\n')
            #             print(self.tool.replace(item))
            #             floor += 1
            content = '\n' + self.tool.replace(item) + '\n'
            contents.append(content)
        return contents

    def setFileTitle(self, title):
        if title is not None:
            self.file = open(title + ".txt", "w+")
        else:
            self.file = open(self.defaultTitle + ".txt", "w+")

    def writeData(self, contents):
        #         向文件写入每一楼的信息
        for item in contents:
            if self.floorTag == '1':
                # 楼之间的分隔符
                floorLine = '\n' + str(self.floor) + '------------\
------------------------------------------------------------\n'
                self.file.write(floorLine)
            print(item)
            self.file.write(item)
            self.floor += 1

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print('URL已失效，请重试')
            return
        try:
            print("该帖子共有" + str(pageNum) + "页")
            # 这里为了测试直写了两页的数据
            # really page = pageNum
            for i in range(1, 2):
                print("正在写入第" + str(i) + "页数据")
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError as e:
            print(e.reason)
        finally:
            print("写入任务完成")


baseURL = 'http://tieba.baidu.com/p/3138733512'
seeLZ = input('是否只获取楼主发言，是输入1，否输入0\n')
floorTag = input('是否写入楼层信息，是输入1，否输入0\n')
bdtb = BDTB(baseURL, seeLZ, floorTag)

bdtb.start()
