# encoding: utf-8
"""
@contact: lucky9322@163.com
@project: PYLesson
@software: PyCharm
@file: Tool.py
@time: 2017/11/11 下午8:42
"""
import re


class Tool(object):
    # 去除image标签，7位长空格
    removeImg = re.compile(r'<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile(r'<a.*?>|</a>')
    # 把换行符换成 \n
    replaceLine = re.compile(r'<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile(r'<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile(r'<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, '', x)
        x = re.sub(self.removeAddr, '', x)
        x = re.sub(self.replaceLine, '\n', x)
        x = re.sub(self.replaceTD, '\t', x)
        x = re.sub(self.replacePara, '\n    ', x)
        x = re.sub(self.replaceBR, '\n', x)
        x = re.sub(self.removeExtraTag, '', x)
        # strip()将前后多余内容删除
        return x.strip()
