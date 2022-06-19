import os
import time
from github import Github

# First create a Github instance:
token = os.environ["git_token"]
# Github Enterprise with custom hostname
g = Github(token)
repo = g.get_repo("IceKyrin/auto_anime_info")

with open("info.sqlite3") as f:
    info = f.read()
repo.update_file("info.sqlite3", "update:%s" % time.localtime(), info, branch="master")
