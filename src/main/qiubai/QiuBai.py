# encoding: utf-8
"""
@contact: lucky9322@163.com
@project: PYLesson
@software: PyCharm
@file: QiuBai.py
@time: 2017/11/10 下午2:30
"""
'''
糗百24小时爆笑笑话

获取每条段子的 发布人，段子内容，好笑数，评论数
'''
import requests
from bs4 import BeautifulSoup


# page = 1
# url = 'http://www.qiushibaike.com/hot/page/' + str(page)
#
# try:
#     response = requests.get(url)
#     bsObj = BeautifulSoup(response.content, "html5lib")
#     jokeContent = bsObj.find('div', {"id": "content-left"})
#     jokeList = jokeContent.find_all('div', {"class": "article"})
#     # print(len(jokeList))
#     for itemJoke in jokeList:
#         # print(itemJoke)
#
#         authorObj = itemJoke.find('div', {'class': 'author clearfix'})
#         author = authorObj.find('a', {'onclick': "_hmt.push(['_trackEvent','web-list-author-text','chick'])"})
#         authorName = ''
#         if author is not None:
#             authorName = author.find('h2').text
#
#         jokeDetailObj = itemJoke.find('a', {'onclick': "_hmt.push(['_trackEvent','web-list-content','chick'])"})
#         jokeDetail = ''
#         if jokeDetailObj is not None:
#             jokeDetail = jokeDetailObj.find('div', {'class': "content"}).find('span').text
#
#         interactObj = itemJoke.find('div', {'class': "stats"})
#         funnyObj = interactObj.find('span', {'class': "stats-vote"})
#         funnyNum = ''
#         if funnyObj is not None:
#             funnyNum = funnyObj.find('i', {'class': "number"}).text
#
#         commentObj = interactObj.find('span', {'class': "stats-comments"})
#         commentNum = ''
#         if commentObj is not None:
#             commentNum = commentObj.find('a').find('i').text
#         print(authorName, jokeDetail, funnyNum + "好笑", commentNum + "评论" + "\n===============================")
# except requests.RequestException  as e:
#     print(e)
#

class QSBK(object):
    def __init__(self):
        self.pageIndex = 1
        # 存放段子的变量，每一个元素是每一页的段子
        self.stories = []
        # 程序是否继续运行
        self.enable = False

    # 传入某一页索引所得页面代码
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            response = requests.get(url)
            return response.content
        except requests.RequestException  as e:
            print(e)
            return None

    # 传入某一页索引，返回本页段子列表
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print('页面加载失败')
            return None

        pageStories = []

        bsObj = BeautifulSoup(pageCode, "html5lib")
        jokeContent = bsObj.find('div', {"id": "content-left"})
        jokeList = jokeContent.find_all('div', {"class": "article"})
        # print(len(jokeList))
        for itemJoke in jokeList:
            # print(itemJoke)

            authorObj = itemJoke.find('div', {'class': 'author clearfix'})
            author = authorObj.find('a', {'onclick': "_hmt.push(['_trackEvent','web-list-author-text','chick'])"})
            authorName = ''
            if author is not None:
                authorName = author.find('h2').text

            jokeDetailObj = itemJoke.find('a', {'onclick': "_hmt.push(['_trackEvent','web-list-content','chick'])"})
            jokeDetail = ''
            if jokeDetailObj is not None:
                jokeDetail = jokeDetailObj.find('div', {'class': "content"}).find('span').text

            interactObj = itemJoke.find('div', {'class': "stats"})
            funnyObj = interactObj.find('span', {'class': "stats-vote"})
            funnyNum = ''
            if funnyObj is not None:
                funnyNum = funnyObj.find('i', {'class': "number"}).text

            commentObj = interactObj.find('span', {'class': "stats-comments"})
            commentNum = ''
            if commentObj is not None:
                commentNum = commentObj.find('a').find('i').text
            # print(authorName, jokeDetail, funnyNum + "好笑", commentNum + "评论" + "\n===============================")
            pageStories.append(
                [authorName.strip('\n'), jokeDetail.strip('\n'), funnyNum.strip('\n'), commentNum.strip('\n')])

        return pageStories

    def loadPage(self):
        # 如果当前未看的页数少于两页，则加载新一页
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                # 将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    # 调用该方法，每次敲回撤打印输出一个段子
    def getOneStory(self, pageStories, page):
        # 遍历一页的段子
        for story in pageStories:
            inputK = input()
            self.loadPage()
            if inputK == 'Q':
                self.enable = False
                return
            print("第%d页\t发布人:%s\t好笑:%s\t评论:%s\n%s" % (page, story[0], story[2], story[3], story[1]))

    def start(self):
        print("正在读取糗事百科,按回车查看新段子，Q退出")
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, nowPage)


spider = QSBK()
spider.start()
