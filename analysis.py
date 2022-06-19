import json
import sqlite3

import demjson
from skylark import Database, Model, Field, PrimaryKey


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
    platform = Field()
    name = Field()
    name_cn = Field()
    season = Field()
    date = Field()


Database.set_dbapi(sqlite3)
Database.config(db='anime.sqlite3', user='', passwd='')


def update_bangumi(b_raw):
    b_id = b_raw["b_id"]
    data = json.loads(b_raw["b_raw"])
    if "platform" in data.keys():
        if Bangumi.findone(b_id=b_id):
            Bangumi.at(b_id).update(platform=data["platform"], name=data["name"], name_cn=data["name_cn"],
                                    date=data["date"]).execute()
            print("update id:%s success" % b_id)
        else:
            Bangumi.create(b_id=b_id, platform=data["platform"], name=data["name"], name_cn=data["name_cn"],
                           date=data["date"])
            print("insert id:%s success" % b_id)


def update_tmdb(t_raw):
    if t_raw["t_raw"] != "empty":
        b_id = t_raw["b_id"]
        data = demjson.decode(t_raw["t_raw"].replace("True", "true").replace("False", "false").replace("None", "\"\""))
        if data["t_id"] != "0":
            name = data["original_title"] if "original_title" in data.keys() else ""
            name_cn = data["title"] if "title" in data.keys() else data["name"]
            num_season = "01" if data["tag"] == "movie" else str(data["number_of_seasons"]).zfill(2)
            date = data["release_date"] if "release_date" in data.keys() else data["first_air_date"]
            if Tmdb.findone(b_id=b_id):
                Tmdb.at(b_id).update(t_id=data["t_id"], name=name, platform=data["tag"],
                                     name_cn=name_cn, season=num_season, date=date).execute()
                print("update:%s" % t_raw["b_id"])
            else:
                Tmdb.create(b_id=b_id, t_id=data["t_id"], platform=data["tag"], name=name,
                            name_cn=name_cn, season=num_season, date=date)
                print("insert:%s" % t_raw["b_id"])


def update(start_id):
    raws = Raw.findall(Raw.b_id > start_id)
    for raw in raws:
        update_bangumi(raw)
        update_tmdb(raw)
