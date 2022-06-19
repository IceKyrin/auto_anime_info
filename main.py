import analysis
import extract
import tmdb
from b_spider import Bspider

if __name__ == "__main__":
    Bspider(10)
    tmdb.run(380000)
    analysis.update(380000)
    extract.run()
