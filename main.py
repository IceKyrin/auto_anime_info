import os
import analysis
import extract
import tmdb
from b_spider import Bspider

if __name__ == "__main__":
    api_key = os.environ["api_key"]
    Bspider(10)
    tmdb.run(380000, api_key)
    analysis.update(380000)
    extract.run()
