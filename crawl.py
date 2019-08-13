# -*- coding: utf-8 -*-
"""
  Create by leiSong on 2019/8/8 19:01 
  @Email : leisong01@qq.com
  @File : crawl.py 
  @description: 
"""
import requests
import re
import random


def agent():
    USER_AGENT_LIST = [
        'MSIE (MSIE 6.0; X11; Linux; i686) Opera 7.23',
        'Opera/9.20 (Macintosh; Intel Mac OS X; U; en)',
        'Opera/9.0 (Macintosh; PPC Mac OS X; U; en)',
        'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
        'Mozilla/4.76 [en_jp] (X11; U; SunOS 5.8 sun4u)',
        'iTunes/4.2 (Macintosh; U; PPC Mac OS X 10.2)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0) Gecko/20100101 Firefox/5.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0',
        'Mozilla/4.77 [en] (X11; I; IRIX;64 6.5 IP30)',
        'Mozilla/4.8 [en] (X11; U; SunOS; 5.7 sun4u)'
    ]
    header = {
        'User-Agent': random.choice(USER_AGENT_LIST)
    }
    return header


class Crawl89ip():
    url = 'http://www.89ip.cn/index_%s.html'
    root_pattern = '<tr>([\s\S]*?)</tr>'
    ip_pattern = '<td>([\s\S]*?)</td>'

    def __fetch_Content(self, url):
        htmls = requests.get(url).content.decode('utf-8')
        r = re.findall(Crawl89ip.root_pattern, htmls)
        if len(r) == 1:
            return None
        return htmls

    def __analysis(self, htmls):
        r = re.findall(Crawl89ip.root_pattern, htmls)
        anchors = []
        for item in range(1, len(r)):
            res = re.findall(Crawl89ip.ip_pattern, r[item])
            anchor = {
                'ip': res[0].strip(),
                'port': res[1].strip(),
                'last_time': res[4].strip()
            }
            anchors.append(anchor)
        return anchors

    def main(self):
        i = 1
        res = []
        while i:
            htmls = self.__fetch_Content(Crawl89ip.url % i)
            # print(Crawl89ip.url % i)
            if htmls == None:
                break
            res.extend(self.__analysis(htmls))
            i += 1
        print(res)
        return res


class CrawlXC():
    url = 'https://www.xicidaili.com/wt'
    root_pattern = '<tr class.*>([\s\S]*?)</tr>'
    ip_pattern = '<td>([\s\S]*?)</td>'

    def __fetch_Content(self, url):
        htmls = requests.get(url, headers=agent()).content.decode('utf-8')
        return htmls

    def __analysis(self, htmls):
        r = re.findall(CrawlXC.root_pattern, htmls)
        anchors = []
        for item in range(1, len(r)):
            res = re.findall(Crawl89ip.ip_pattern, r[item])
            anchor = {
                'ip': res[0].strip(),
                'port': res[1].strip(),
                'last_time': res[5].strip()
            }
            anchors.append(anchor)
        return anchors

    def main(self):
        htmls = self.__fetch_Content(CrawlXC.url)
        res = self.__analysis(htmls)
        print(res)
        return res
