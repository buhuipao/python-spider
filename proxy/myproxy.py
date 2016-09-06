#coding:utf-8

import urllib2
import re
import time
import threading
import cookielib
import random

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

ProxyList = []
CheckedList= []
targets=['http://www.xicidaili.com/nn/1', 'http://www.xicidaili.com/nn/2', 'http://www.xicidaili.com/nn/3', 'http://www.xicidaili.com/nn/4']
get_count = 0
check_count = 0
pattern = re.compile(r'<tr class.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', re.S)

class ProxyGet(threading.Thread):
     #初始化
    def __init__(self, target):
        threading.Thread.__init__(self)
        self.target = target

     #组装头部，得到request
    def get_Proxy(self):
        print(u"目标网址: %s" % self.target)
        url = self.target
        header = {
                'User-Agent': random.choice(USER_AGENTS),
                'Referer': 'http://www.xicidaili.com/wn/'
                }
        request = urllib2.Request(url, headers = header)

     #解析西刺的代理页地址
        result = urllib2 .urlopen(request)
        contents = result.read().decode('utf-8')
        matchs = re.findall(pattern, contents)
        for match in matchs:
            ip = match[0]
            port = match[1]
            protocol = match[3]
             #定义全局变量，不然被局部函数修改过的变量会被认为是局部变量，报错
            global get_count
            if protocol == 'HTTP':
                ProxyList.append(ip + ':' + port)
                get_count += 1
                print(u"恭喜你抓到第%d个代理%s\n" % (get_count, ip+':'+port))

    def run(self):
        self.get_Proxy()

class CheckProxy(threading.Thread):
    def __init__(self, ProxyList):
        threading.Thread.__init__(self)
        self.proxyList = ProxyList
        self.timeout = 5
        self.testURL = "https://baidu.com"

    def check_proxy(self):
        cj = cookielib.CookieJar()
        cookies = urllib2.HTTPCookieProcessor(cj)
        for proxy in self.proxyList:
            proxy_handler = urllib2.ProxyHandler({"http":'http://'+proxy})
            opener = urllib2.build_opener(cookies, proxy_handler)
            opener.addheaders = [('User-Agent', random.choice(USER_AGENTS))]
            urllib2.install_opener(opener)
             #定义全局变量，不然被局部函数修改过的变量会被认为是局部变量，报错
            global check_count
            t = time.time()
            try:
                request = opener.open(self.testURL, timeout=self.timeout)
                timeused = time.time() - t
                result = request.read().decode('utf-8')
                print result
                check_count += 1
                print(u"干的漂亮！你抓来的第%d个代理%s通过检测, 花费时间%fs\n" % (check_count, proxy, timeused))
                CheckedList.append(proxy)
            except Exception, e:
                check_count += 1
                print(u"很尴尬-_-，你抓来的第%d个代理%s没能通过检查\n" % (check_count, proxy))

    def run(self):
        self.check_proxy()

if __name__ == "__main__":
    getThreads = []
    checkThreads = []

 #对每个自由代理网站开启一个线程来抓取代理ip
for target in targets:
     proxy = ProxyGet(target)
     getThreads.append(proxy)

for getThread in getThreads:
    getThread.start()

#此处必须用join阻塞(解析速度很快不用担心)，不然下面的代理检查会出错(抓取代理为空)
#前面urllib2的解析用了timeout不用担心堵死
for getThread in getThreads:
    getThread.join()

print(u"共抓取%s个代理" % len(ProxyList))

 #开启20+1个线程检查代理ip
t = len(ProxyList) / 20
for l in list(ProxyList[i:i+t] for i in xrange(0,len(ProxyList), t)):
    check = CheckProxy(l)
    checkThreads.append(check)

for checkThread in checkThreads:
    checkThread.start()

#防止阻塞urllib2也用了timeout，但此处还是不用阻塞
for checkThread in checkThreads:
    checkThread.join()

print(u"共有%s个代理通过检查\n" % len(CheckedList))
print(u"共有%d个代理被抓到,还不错有%d个通过检查！"% (get_count, len(CheckedList)))

"""
    def choice_proxy(self, proxies):
        proxy = random.choice(proxies)
        if proxy == None:
            proxy_hander= urllib2.ProxyHandler({})
        else:
            proxy_hander= urllib2.ProxyHandler({'http':proxy})
        opener = urllib2.build_opener(proxy_hander)
        opener.addheaders = [('User-Agent', headers['User-Agent'])]
        urllib2.request.install_opener(opener)
        print(u'智能选择代理: %s' % ('本地' if proxy == None else proxy))
"""
