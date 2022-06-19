import shutil
import sqlite3


def clean():
    cur = sqlite3.connect("anime.sqlite3")
    cur.execute("vacuum")
    cur.commit()
    cur.close()


def run():
    clean()
    shutil.copyfile("anime.sqlite3", "info.sqlite3")
    cur = sqlite3.connect("info.sqlite3")
    cur.execute("DROP TABLE RAW")
    cur.execute("vacuum")
    cur.commit()
    cur.close()


if __name__ == "__main__":
    clean()
    run()
