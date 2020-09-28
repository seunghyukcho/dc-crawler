from tap import Tap

from dcinside import Crawler
from dcinside.exception import *


class ArgumentParser(Tap):
    gallery: str  # Name of gallery (etc. leagueoflegends3)
    start_idx: int = 1  # Start index of gallery page
    end_idx: int  # End index of gallery page
    chrome_driver: str  # Path to chrome driver


if __name__ == "__main__":
    args = ArgumentParser().parse_args()
    crawler = Crawler(args.chrome_driver, timeout=60, retry=True)

    for page_idx in range(args.start_idx, args.end_idx + 1):
        try:
            post = crawler.crawl(args.gallery, page_idx)
            print(post["title"])
            print(post["content"])
            for comment in post["comments"]:
                print(comment)
        except (ServerException, DeletedPostException) as e:
            print(e)
