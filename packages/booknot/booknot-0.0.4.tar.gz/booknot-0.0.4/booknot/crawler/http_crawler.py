from datetime import datetime

import requests
from bs4 import BeautifulSoup

from booknot.crawler.crawler import Crawler
from booknot.crawler.metadata import Metadata


class HttpCrawler(Crawler):

    def __init__(self, session: requests.Session):
        self.session = session

    def fetch(self, url: str) -> Metadata:
        r = self.session.get(url)
        content = r.content
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.head.title.string
        description = soup.head.find('meta', property="og:description")["content"]
        now = datetime.now()

        return Metadata(url=url, title=title, description=description, capture_date=now)
