# -*- coding: utf-8 -*-
"""
  Create by leiSong on 2019/8/9 08:41 
  @Email : leisong01@qq.com
  @File : test.py 
  @description: 
"""
import aiohttp
import time
import random
import asyncio
import requests


class TestProxy():
    def __init__(self):
        self.url = 'http://www.qq.com/'
        self.timeout = 10

    async def request(self, session, proxy):
        async with session.get(self.url, proxy=proxy, timeout=self.timeout) as response:
            return response.status == 200

    async def test(self, id, ip, port):
        proxy = 'http://%s:%s' % (ip, port)
        try:
            conn = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=conn) as session:
                print("当前测试第%s个代理：%s" % (id, proxy))
                time.sleep(random.randint(1, 3))
                code = await self.request(session, proxy)
                if code:
                    return True, id
                else:
                    return False, id
        except:
            return False, id

    def __test(self, id, ip, port):
        proxies = {
            'http': 'http://%s:%s' % (ip, port)
        }
        try:
            wb_data = requests.get(url='http://www.baidu.com', proxies=proxies, timeout=10)

            print(wb_data.status_code)
            if wb_data.status_code == 200:
                return True, id
            else:
                return False, id

        except Exception:
            print(Exception)
            return False, id

    def go(self, ipsFromsql):
        for i in range(len(ipsFromsql)):
            print(ipsFromsql[i])
            self.__test(ipsFromsql[i][1], ipsFromsql[i][2])

    def main(self, proxy_list):
        tasks = [asyncio.ensure_future(self.test(proxy[0], proxy[1], proxy[2])) for proxy in proxy_list]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        print([i.result() for i in tasks])
        return [i.result() for i in tasks]
