import json
import logging
import sqlite3
import requests
from skylark import Database, Model, Field, PrimaryKey

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ApplewebKit/538.36 (KHtml, like Gecko) Chrome/90.0.3987.163 Safari/537.36',
}


class Raw(Model):
    b_id = PrimaryKey()
    a_raw = Field()
    b_raw = Field()
    t_raw = Field()


class Bangumi(Model):
    b_id = PrimaryKey()
    platform = Field()
    name = Field()
    name_cn = Field()
    date = Field()


class Tmdb(Model):
    b_id = PrimaryKey()
    t_id = Field()
    name = Field()
    name_cn = Field()
    season = Field()
    date = Field()


def get_html(url):
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    html = s.get(url=url, headers=header, timeout=5).text  # 你需要的网址
    return html


Database.set_dbapi(sqlite3)
Database.config(db='anime.sqlite3', user='', passwd='', check_same_thread=False)


def search(query, tag, api_key):
    url = "https://api.themoviedb.org/3/search/%s?api_key=%api_key&query=%s&page=1&language=zh" % (api_key, tag, query)
    return get_html(url)


def get_detail(mv_id, tag, api_key):
    api = "https://api.themoviedb.org/3/%s/" % tag
    url = api + str(mv_id) + "?api_key=%s&language=zh" % api_key
    return get_html(url)


def add_empty(b_id):
    Raw.at(b_id).update(t_raw="empty").execute()
    print("b_id:%s is empty" % b_id)


def add_data(b_id, api_key):
    b_raw = json.loads(Raw.findone(b_id=b_id)["b_raw"])
    if "name" in b_raw.keys():
        name = b_raw["name"]
        tag = "movie"
        res = json.loads(search(name, tag, api_key))
        if "total_results" in res:
            if res["total_results"] == 0:
                tag = "tv"
                res = json.loads(search(name, tag, api_key))
            if res["total_results"]:
                movie_id = res["results"][0]["id"]
                detail = json.loads(get_detail(movie_id, tag, api_key))
                detail["tag"] = tag
                detail["t_id"] = movie_id
                Raw.at(b_id).update(t_raw=json.dumps(detail)).execute()
                print("b_id:%s,t_id:%s" % (b_id, movie_id))
            else:
                add_empty(b_id)
        else:
            add_empty(b_id)
    else:
        add_empty(b_id)


def run(start_id, api_key):
    try:
        b_ids = [x["b_id"] for x in Raw.findall(Raw.b_id > start_id)]
        exists = [x["b_id"] for x in Raw.findall(Raw.t_raw != "")]
        for i in b_ids:
            if i not in exists:
                try:
                    add_data(i, api_key)
                except Exception as e:
                    print(e)
    except Exception as e:
        logging.info(e)
