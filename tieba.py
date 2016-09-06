#!/bin/env python
#-*- coding:utf-8 -*-

import urllib2
import urllib
import re

class TIEBA(object):
    
    def __init__(self, baseurl, seelz):
        self.baseurl = baseurl
        self.seelz = '?see_lz=' + str(seelz)

    def getPage(self, pagenum):
        try:
            url = self.baseurl + self.seelz + '&pn' + str(pagenum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request).read().decode('utf-8')
            #print response
            return response
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接百度贴吧出错，错误为：",+ e.reason
                return None

    def getTitle(self):
        page = self.getPage(1)
        pattern = re.compile(r'<h3 class="core_title_txt pull-left text-overflow.*?>(.*?)</h3>',re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getPageNum(self):
        page = self.getPage(1)
        pattern = re.compile(r'<li class="l_reply_num".*?</span>.*?>(.*?)</span>',re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None
    
    def getPageContent(self):
        page = self.getPage(1)
        pattern = re.compile(r'<div id="post_content_.*?>(.*?)</div>')
        removeImg = re.compile(r'<img .*?>',re.S)
        removeLink = re.compile(r'(<a .*?>|</a>)',re.S)
        items = re.findall(pattern, page)
        count = 0
        for item in items:
            count += 1
            #移除图片
            item = re.sub(removeImg, "", item)
            #移除超链接
            item = re.sub(removeLink,"",item)
            #把多个连续的<br>换成一个换行
            item = re.sub(r'<br>+', "\n",item)
            #移除多余换行
            item = re.sub(r'\n+', "\n",item)
            #移除多余的空格,并在每个楼层的开始增加两个空格
            item = re.sub(r'( +|\t)', '', item)
            item = re.sub(r'\n', '\n  ', item)
            if '\n' not in item:
                print u"\n第%d楼-----------------------------------------------------------------------------------\n   %s" % (count,item)
            else:
                print u"\n第%d楼-----------------------------------------------------------------------------------%s" % (count,item)


    #def writeData(self, content):


baseurl = 'http://tieba.baidu.com/p/3138733512'
bdtb = TIEBA(baseurl,1)
bdtb.getTitle()
bdtb.getPageNum()
bdtb.getPageContent()
