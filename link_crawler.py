import time

from threading import Thread

from downloader import Downloader
from utils import get_robot_txt

SLEEP_TIME = 1

def link_crawler(
                 seed_url, crawl_queue, scrape_callback, cache,
                 num_retries=1, max_threads=1
                 ):

    crawl_queue.push(seed_url)

    rp = get_robot_txt(seed_url)

    downloader = Downloader(num_retries=num_retries, timeout=2, cache=cache)

    def thread_process():
        while True:
            try:
                url = crawl_queue.pop()
            except KeyError:
                break

            if rp.can_fetch(url):
                html = downloader(url)
                links = []
                if scrape_callback:
                    links.extend(scrape_callback(url, html) or [])
                    for link in links:
                        crawl_queue.push(link)
                crawl_queue.complete(url)
            else:
                print('robot.txt doesnt allow')

    threads = []
    while threads and crawl_queue.peek():
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

            while (len(threads) < max_threads) and crawl_queue:
                thread = Thread(target=thread_process, daemon=True)
                thread.start()
                threads.append(thread)
            time.sleep(SLEEP_TIME)
