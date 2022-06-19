import logging
import re
import sqlite3

import requests
from retry import retry
from skylark import Database, Model, Field, PrimaryKey


class Bspider():
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ApplewebKit/538.36 (KHtml, like Gecko) Chrome/90.0.3987.163 Safari/537.36',
    }
    api_header = {"user-agent": "database"}

    class Bangumi(Model):
        b_id = PrimaryKey()
        raw = Field()

    Database.set_dbapi(sqlite3)
    Database.config(db='anime.sqlite3', user='', passwd='', check_same_thread=False)

    def __init__(self, pages):
        for i in range(1, pages + 1):
            print("getting page:%s" % i)
            self.run(i)

    def get_html(self, url):
        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        html = s.get(url=url, headers=header, timeout=5).text  # 你需要的网址
        s.close()
        return html

    @retry(tries=3, delay=5)
    def get_page(self, page):
        url = "https://bangumi.tv/anime/browser/?sort=date&page=%s" % page
        return self.get_html(url)

    @retry(tries=3, delay=5)
    def get_info(self, b_id):
        bangumi_url = "https://api.bgm.tv/v0/subjects/"
        res = requests.get(bangumi_url + str(b_id), headers=api_header).text
        return res

    def run(self, page):
        try:
            ids = re.findall("id=\"item_(\d+)\"", get_page(page + 1))
            for b_id in ids:
                if Bangumi.findone(b_id=b_id):
                    raw = self.get_info(b_id)
                    Bangumi.at(b_id).update(raw=raw).execute()
                    print("update id:%s success" % b_id)
                else:
                    raw = self.get_info(b_id)
                    Bangumi.create(b_id=b_id, raw=raw)
                    print("insert id:%s success" % b_id)
        except Exception as e:
            logging.info(e)
