#coding: utf-8
__author__ = 'liufei'

import sys, time
from bs4 import BeautifulSoup as BS
from data.data import data
from lib.base import base
reload(sys)
sys.setdefaultencoding('utf-8')

class kuaidaili(base):
    def __init__(self):
        self.data = data()
        self.base = base()
        self.url = self.data.kuaidaili
        self.bs = None

    def getLatestFreeURL(self):
        '''
                # 获取该网站最新免费代理页面URL
        '''
        urls = []
        for i in range(self.data.kuaidaili_pagescount):
            urls.append(self.url % (i+1))
        return urls

    def getProxies(self, url):
        '''
                # 获取目标页面中免费代理
        '''
        html = self.base.request_url(url)
        bs = BS(html, from_encoding="utf8")
        ip = bs.findAll(name="td", attrs={"data-title": "IP"})
        port = bs.findAll(name="td", attrs={"data-title": "PORT"})
        level = bs.findAll(name="td", attrs={"data-title": "匿名度"})
        type = bs.findAll(name="td", attrs={"data-title": "类型"})
        proxies = []
        proxy = zip(ip, port, level, type)
        for p in proxy:
            # if "匿名" in p[2].text and "HTTPS" in p[3].text:
            if "匿名" in p[2].text:
                proxies.append(p[0].text+":"+p[1].text)
        return proxies

    def save(self, filename, mode):
        latestUrls = self.getLatestFreeURL()
        result = []
        for url in latestUrls:
                proxies = self.getProxies(url)
                if proxies:
                    result += proxies
                else:
                    break
        base.sava_result(filename, result, mode)
        print time.strftime("%Y-%m-%d %X", time.localtime()) + " | [快代理] - Proxy count is %d!" % len(result)

if __name__ == "__main__":
    filename = "/Users/luca/WebServer/Documents/kuaidaili.txt"
    while True:
        kdl = kuaidaili()
        kdl.save(filename)
        time.sleep(180)

