from pathlib import Path

from webnovel import WebnovelBot
from webnovel.api import ParsedApi
from webnovel.models import Novel
from webnovel.tools import UrlTools

from .concurrent import ConcurrentActionsController
from .database import WebNovelData
from .epub import Epub
from .models import Chapter
from .template import NovelSaveTemplate
from .tools import UiTools
from .ui import Loader


class WebNovelSave(NovelSaveTemplate):
    timeout: int = 60

    _api: ParsedApi = None

    def __init__(self, url, username=None, password=None, directory=None):
        super(WebNovelSave, self).__init__(url, username, password, directory)

        self.novel_id = UrlTools.from_novel_url(url)

    def update(self, force_cover=False):
        # get api
        api = self.get_api()

        with Loader('Scraping novel'):
            novel = Novel.from_url(UrlTools.to_novel_url(self.novel_id))

            # obtain table of contents
            toc = api.toc(self.novel_id)

        if force_cover or not self.cover_path().exists():
            # download cover
            cover_data = UiTools.download(novel.cover_url, desc=f'Downloading cover {novel.cover_url}')
            with self.cover_path().open('wb') as f:
                f.write(cover_data.getbuffer())

        # # #
        # update data
        data = self.open_db()

        with Loader('Update novel'):
            data.info.set_info(novel)

        with Loader('Update volumes'):
            for volume, chapters in toc.items():
                data.volumes.set_volume(volume, [c.id for c in chapters])

        with Loader('Update pending') as brush:
            saved = data.chapters.all()
            pending = list({self.to_chapter(c) for v in toc.values() for c in v if not c.locked}.difference(saved))

            brush.desc += f' ({len(pending)})'

            data.pending.truncate()
            data.pending.put_all([c for c in pending])

    def download(self, thread_count=4, limit=None):
        """
        Download remaining chapters
        """
        data = self.open_db()
        pending = data.pending.all()
        if len(pending) <= 0:
            print('[✗] No pending chapters')
            return

        # limiting number of chapters downloaded
        if limit is not None and limit < len(pending):
            pending = pending[:limit]

        api = self.get_api()

        with Loader(f'Populating tasks ({len(pending)})', value=0, total=len(pending)) as brush:

            def task(novel_id, chapter_id):
                return self.to_chapter(api.chapter(novel_id, chapter_id))

            # initialize controller
            controller = ConcurrentActionsController(thread_count, task=task)
            for chapter in pending:
                controller.add(self.novel_id, chapter.index)

            # start downloading
            for chapter in controller.iter():
                # update brush
                brush.value += 1
                brush.desc = f'[{brush.value}/{brush.total}] {chapter.url}'

                # get data
                data.chapters.insert(chapter)

                # at last
                data.pending.remove(chapter.index)

    def create_epub(self):
        """
        Create epub with current data
        """
        data = self.open_db()

        with Loader('Create epub'):
            Epub().create(
                novel=data.info.get_info(),
                cover=self.cover_path(),
                volumes=data.volumes.all(),
                chapters=data.chapters.all(),
                save_path=self.path()
            )

    def get_api(self) -> ParsedApi:
        """
        if api exists returns existing
        else creates api according to provided credentials

        :return: Api according to access level
        """
        if self._api is None:
            if self.should_signin():
                # sign in to get access token
                webnovel = WebnovelBot(timeout=self.timeout)
                webnovel.driver.get(UrlTools.to_novel_url(self.novel_id))
                webnovel.signin(self.username, self.password)

                # get api with token
                self._api = webnovel.create_api()
                webnovel.close()
            else:

                # full credentials not provided so
                # create api with no token create
                self._api = ParsedApi()

        return self._api

    def open_db(self):
        return WebNovelData(self.path())

    def should_signin(self):
        return self.username is not None and self.password is not None

    def cover_path(self) -> Path:
        return self.path() / Path('cover.jpg')

    def path(self):
        path = Path(self.user.directory.get()) / Path(f'n{self.novel_id}')
        path.mkdir(parents=True, exist_ok=True)

        return path

    def to_chapter(self, wchapter):
        return Chapter(
            index=wchapter.id,
            no=wchapter.no,
            title=wchapter.title,
            paragraphs=wchapter.paragraphs,
            url=wchapter.url
        )
