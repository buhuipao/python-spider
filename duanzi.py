#!/bin/env python
#-*- coding:utf-8 -*-

import urllib2
import urllib
import re
import thread

class DZ(object):
    def __init__(self):
        self.pagenum = 1
        self.user_agent = 'Mazilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        self.stories = []
        self.enable = False
        self.pageIndex = 1
    #传入某一页的索引获取页面代码
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接错误，原因：",e.reason
                return None
    
    #解析页面的段子
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print u"页面加载失败..."
            return None
        else:
            pattern = re.compile(r'<div.*?author clearfix">.*?<h2>(.*?)</h2>.*?class="content">(.*?)</div>.*?class="number">(.*?)</i>.*?class="number">(.*?)</i>',re.S)
            items = re.findall(pattern, pageCode)
            pageStories = []
            for item in items:
                haveImg = re.search("thumb",item[1])
                if not haveImg:
                    replaceBR = re.compile(r'<br/>')
                    #替换段子内容中的<br/>为换行
                    text = re.sub(replaceBR,"\n",item[1])
                    pageStories.append([item[0].strip(), text.strip(), item[2].strip(), item[3].strip()])
            return pageStories

    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                #获取新的一页
                pageStories = self.getPageItems(self.pageIndex)
                #将新获取的放到总list中
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1


    #调用此方法，每敲击一次回车输出一个段子
    def getOnestory(self, pageStories, page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print u"第%d页\t发布人:%s\t有%s笑过\t被评论%s次\n%s" % (page, story[0], story[2], story[3], story[1])

    #开始
    def start(self):
        print u"载入内涵段子请稍等,按回车查看下一条段子,Q退出"
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOnestory(pageStories,nowPage)

spider = DZ()
spider.start()
