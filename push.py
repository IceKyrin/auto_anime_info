import os
import time
import base64
from github import Github


def get_file(image_path):
    with open(image_path, 'rb') as f:
        data = f.read()
    return str(data)


def run(token):
    g = Github(token)
    repo = g.get_repo("IceKyrin/auto_anime_info")
    repo.update_file("anime.sqlite3", "update", get_file("anime.sqlite3"), repo.get_contents("anime.sqlite3").sha,
                     branch="master")
    repo.update_file("info.sqlite3", "update", get_file("info.sqlite3"), repo.get_contents("info.sqlite3").sha,
                     branch="master")
