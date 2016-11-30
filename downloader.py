
import requests


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

    def download(self, url, num_retries):
        print('Downloading ' + url)
        try:
            request = requests.get(url, timeout=self.timeout)
            html = request.text
            request.raise_for_status()
        except Exception as e:
            err = str(e)
            code = int(err.split(' ')[0])
            html = ''
            if num_retries > 0 and 500 <= code < 600:
                # retry 5XX HTTP errors
                return self.download(url, num_retries - 1)

        return {'html': html}