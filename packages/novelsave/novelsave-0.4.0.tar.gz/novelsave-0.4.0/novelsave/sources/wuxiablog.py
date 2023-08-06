import re
from typing import Tuple, List

from .source import Source
from ..models import Novel, Chapter


class WuxiaBlog(Source):
    base = 'https://www.wuxia.blog'

    @staticmethod
    def of(url: str) -> bool:
        return url[:len(WuxiaBlog.base)] == WuxiaBlog.base

    def novel(self, url: str) -> Tuple[Novel, List[Chapter]]:
        soup = self.soup(url)

        author = ''
        for col in soup.find_all('div', {'class': 'col-lg-6'}):
            h4 = col.find('h4').text
            if h4 == 'Author':
                author = col.find('a').text.strip()

        novel = Novel(
            title=soup.find('h4', {'class': 'panel-title'}).text.strip(),
            author=author,
            url=url,
        )

        chapters = []
        for chapter_element in soup.find('tbody', {'id', 'chapters'}).find_all('tr'):
            a = chapter_element.find('a')

            chapter = Chapter(
                title=a.text,
                url=a['href']
            )

            chapters.append(chapter)

        return novel, chapters
