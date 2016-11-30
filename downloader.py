

class Downloader:

    def __init__(self, num_retries, timeout, cache):

        self.timeout = timeout
        self.num_retries = num_retries
        self.cache = cache

    def __call__(self, url):

        result = None

        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                print('html not in cache')
                pass

        if result is None:
            result = self.download(url, num_retries=self.num_retries)
            if self.cache:
                print('save result to cache')
                self.cache[url] = result['html']

        return result['html']