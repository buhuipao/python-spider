#!/bin/env python
#coding:utf-8
import urllib2
import urllib
import re, os
import requests


class Spider(object):

    def __init__(self):
        self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'

    #获取索引界面的内容
    def getPage(self, pageIndex):
        url = self.siteURL + "?page=" + str(pageIndex)
        i_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48',
                'Referer':'https://world.taobao.com'}
        print url
        request = urllib2.Request(url, headers=i_headers)
        response = urllib2.urlopen(request, None, 5)
        return response.read().decode('gbk')
    
    #索引界面所有mm，list格式
    def getMM(self, pageIndex):
        page = self.getPage(pageIndex)
        #第一个是mm爱秀网址，第二是个人主页，第三是名字，第四是年纪，第五是地点
        pattern = re.compile(r'<div class="pic s60".*?<a href="//(.*?)".*?<a class="lady-name" href="//(.*?)".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
             #分别代表mm个人主页链接，名字，芳龄，省份
            contents.append([item[0],item[1],item[2],item[3],item[4]])
        return contents

    #获取MM个人详情页
    def getDetailPage(self, infoURL):
        i_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48',
                'Referer':'https://world.taobao.com'}
        request = urllib2.Request(infoURL, headers=i_headers)
        response = urllib2.urlopen(request, None, 5)
        detail = response.read().decode('gbk')
        return detail

    #获取个人基本信息
    def getBaseInf(self, detail):
        pattern = re.compile(r'<div class="mm-p-info mm-p-base-info">.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?</div>', re.S)
        base_info = re.search(pattern, detail)
        return base_info

    #创建每个mm的文件夹
    def mkdir(self, name):
        path = 'mm' + '/' + name
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print(u"正在为mm%s创建%s目录..." % (name, path))
            os.makedirs(path)
            return True
        else:
            print(u"mm%s的文件夹已存在, 无需创建" % name)
            return False

    #保存个人信息到文件
    def saveInf(self, base_info, name):
        inf_file = name + '/' + name + ".txt"
        info = base_info
        print(u"正将%s的个人信息保存到%s..." % (name, inf_file))
        #with open('inf_file', 'wt', encoding='utf-8') as inf_file:
        #    print('u"基本信息\n昵称：%s\n生日：%s\t\t所在城市：%s\n职业：%s\t\t血型：%s\n学校专业：%s\t\t风格：%s\n\n身高：%s\t三围：%s\tSize：%s\t鞋码：%s", % (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9], info[10], info[11])', file=inf_file)

    #获取爱秀页面上所有的图片URL
    def getImgsURL(self, aixiu_URL):
        i_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48'}
        #proxy = urllib2.ProxyHandler({'http': '182.204.60.117:8118'})
        #opener = urllib2.build_opener(proxy)
        #urllib2.install_opener(opener)
        request = urllib2.Request(aixiu_URL, headers=i_headers)
        response = urllib2.urlopen(request, None, 5)
        aixiu_page = response.read().decode('gbk')
        pattern = re.compile(r'<img .*?src="//(img.alicdn.com/imgextra/i\d.*?)"', re.S)
        imagesURL = re.findall(pattern, aixiu_page)
        return imagesURL

    #传入单个url保存单张照片
    def saveImg(self, imageURL, fileName):
        imageURL = 'https://' + imageURL
        img = urllib.urlopen(imageURL)
        #此处不需要转码为utf-8，因为为二进制数据
        data = img.read()
        f = open(fileName, 'wb')
        f.write(data)
        f.close()

    #通过所有的图片URL, 保存mm爱秀上页面上的所有照片
    def saveImgs(self, imagesURL, name):
        self.mkdir(name)
        number = 1
        print u"发现",name,u"共有",len(imagesURL),u"张照片"
        for imageURL in imagesURL:
            #splitImage= imageURL.split('.')
            fTail = imageURL[-3:]
            fileName = 'mm' + '/' + name + '/' + str(number) + '.' + fTail
            fileExists = os.path.exists(fileName)
            if not fileExists:
                print(u"正在保存mm %s 的第%s张照片..." % (name, str(number)))
                self.saveImg(imageURL, fileName)
            else:
                print(u"mm %s 的第%s张照片已存在无需再次保存" % (name, str(number)))
            number += 1

     #保存单页上的mm照片
    def savePageMM(self, pageIndex):
        items = self.getMM(pageIndex)
        for item in items:
            print(u"\n发现一名淘宝mm，名字叫%s,芳龄%s，她住在%s" % (item[2], item[3], item[4]))
            print(u"正在前往mm%s的主页..." % item[2])
            aixiu_url = 'https://' + item[0]
            infoURL = 'https://' + item[1]+ '&is_coment=false'
            name = item[2]
             #获取mm详细主页
            detail = self.getDetailPage(infoURL)
             #获取mm基础信息
            base_info = self.getBaseInf(detail)
             #保存mm基础信息
            self.saveInf(base_info, name)
             #通过爱秀URL下载爱秀页面解析出所有的照片url
            imgsurl = self.getImgsURL(aixiu_url)
            print(imgsurl)
             #通过url下载照片并保存
            self.saveImgs(imgsurl, name)
    
    def savePages(self, start, end):
        for i in range(start, end+1):
            print(u"正在第%s页寻找mm..." % i)
            self.savePageMM(i)

spider = Spider()
spider.savePages(6,10)
