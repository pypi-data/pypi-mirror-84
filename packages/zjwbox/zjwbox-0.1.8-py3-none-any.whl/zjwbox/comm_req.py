import requests
import parsel, re
import time, random
import asyncio, aiohttp
from tqdm import tqdm
from itertools import product
import eventlet
from faker import Faker
from datetime import datetime


fake = Faker()
fake_ua = fake.user_agent()

class Comm_req(object):

    def __init__(self, urls, headers={"UserAgent": fake_ua}, cookie=None, data=None, 
                        encode="utf-8", mode="get", time_inter=False):
        self.urls = urls
        self.headers = headers
        self.cookie = cookie
        self.data = data
        self.mode = mode
        self.encode = encode
        self.time_inter = time_inter

    async def fask(self, url, mode="get") -> str:
        async with aiohttp.ClientSession() as session:
            if self.mode == "post":
                async with session.post(url, headers=self.headers, timeout=3) as res:
                    return await res.text()
            else:
                async with session.get(url, headers=self.headers, timeout=3) as res:
                    return await res.text()

    def deal(self):
        if isinstance(self.urls, str):
            session = requests.Session()
            self.time_inter = 0
            if self.time_inter:
                self.time_inter = random.choice([0.5, 1, 0.9, 1.5])
                res = session.get(self.urls, headers=self.headers, timeout=5)
                text = res.content.decode(self.encode)
                if self.mode == "post":
                    res = session.post(self.urls, self.headers)
                    text = res.content.decode(self.encode)
                time.sleep(self.time_inter)
                yield text
            else:
                res = session.get(self.urls, headers=self.headers, timeout=5)
                text = res.content.decode(self.encode)
                if self.mode == "post":
                    res = session.post(self.urls, self.headers)
                    text = res.content.decode(self.encode)
                yield text

        else:
            for url in self.urls:
                loop = asyncio.get_event_loop()
                text = loop.run_until_complete( self.fask(url, self.mode) )
                now_time = datetime.now()
                print(f"爬取{url}成功！时间：{now_time}")
                yield text


    def get_page(self):
        result = []
        for page in self.deal():
            result.append(page)
        if result == []:
            return None
        eventlet.monkey_patch()
        now_time = datetime.now()
        if isinstance(self.urls, str):
            print(f"目标1个，成功爬取{len(result)}, 时间：{now_time}")
        else:
            print(f"目标{len(self.urls)}个，成功爬取{len(result)}，时间：{now_time}")
  
        return result
        
           

if __name__ == "__main__":
    urls = ["https://www.baidu.com", "https://www.douban.com", "https://www.zhihu.com"]
    # urls = "https://www.baidu.com"
    c = Comm_req(urls=urls)
    text = c.get_page()
    print(text)

    


