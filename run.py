# -*- coding: utf-8 -*-
"""
  Create by leiSong on 2019/8/8 21:54 
  @Email : leisong01@qq.com
  @File : run.py 
  @description: 
"""
from proxyPool.crawl import Crawl89ip, CrawlXC
from proxyPool.save import SaveToMysql
from proxyPool.test import TestProxy

import time


def crawl(crawlip, savetomysql):
    # 爬取
    savetomysql.openSql()
    ips = crawlip.main()

    for ip in ips:
        savetomysql.main(ip['ip'], ip['port'], ip['last_time'])
    savetomysql.closeSql()
    print('抓取完毕~~~~')


def test(testproxy, savetomysql):
    # 测试
    savetomysql.openSql()
    ipsFromsql = savetomysql.getAll()

    # testproxy.go(ipsFromsql)

    ipsFromsqlCut = [ipsFromsql[i:i+20] for i in range(0, len(ipsFromsql), 20)]

    for i in range(len(ipsFromsqlCut)):
        test_res = testproxy.main(ipsFromsqlCut[i])
        for itemIp in test_res:
            savetomysql.updateMark(itemIp[1], itemIp[0])

    savetomysql.closeSql()
    print('测试完毕~~~~')


if __name__ == '__main__':

    crawl89ip = Crawl89ip()
    crawlxc = CrawlXC()

    savetomysql = SaveToMysql()
    testproxy = TestProxy()

    while True:
        crawl(crawl89ip, savetomysql)
        print('89ip 抓取完毕~~~~')
        crawl(crawlxc, savetomysql)
        print('西刺 抓取完毕~~~~')
        time.sleep(60 * 0.5 * 1)
        test(testproxy, savetomysql)
        time.sleep(60 * 60 * 6)
