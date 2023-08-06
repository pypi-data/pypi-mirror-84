from pathlib import Path

from . import Epub
from .concurrent import ConcurrentActionsController
from .database import NovelData
from .sources import WuxiaWorldCo, BoxNovel, ReadLightNovel
from .template import NovelSaveTemplate
from .tools import StringTools, UiTools
from .ui import Loader


class SourceNovelSave(NovelSaveTemplate):
    def __init__(self, url):
        super(SourceNovelSave, self).__init__(url, None, None)

        self.db = self.open_db()
        self.source = self.parse_source()

    def update(self, force_cover=False):
        # scrape website, get novel info and toc
        with Loader('Scraping novel'):
            novel, chapters = self.source.novel(self.url)

        if force_cover or not self.cover_path().exists():
            # download cover
            data = UiTools.download(novel.thumbnail, desc=f'Downloading cover {novel.thumbnail}')
            with self.cover_path().open('wb') as f:
                f.write(data.getbuffer())

        # update novel information
        with Loader('Update novel'):
            self.db.novel.set(novel)

        # update_pending
        with Loader('Update pending'):
            saved_urls = [chapter.url for chapter in self.db.chapters.all()]

            # so that downloads are ascending
            pending = list({chapter.url for chapter in chapters}.difference(saved_urls))

            self.db.pending.truncate()
            self.db.pending.insert_all(
                pending,
                check=False
            )

    def download(self, thread_count=4, limit=None):
        pending = self.db.pending.all()
        if not pending:
            print('[✗] No pending chapters')
            return

        pending.sort(key=StringTools.collect_integers)

        # limiting number of chapters downloaded
        if limit is not None and limit < len(pending):
            pending = pending[:limit]

        with Loader('Populating tasks', value=0, total=len(pending)) as brush:

            # initialize controller
            controller = ConcurrentActionsController(thread_count, task=self.source.chapter)
            for url in pending:
                controller.add(url)

            # start downloading
            controller.start()

            # wait until downloads are done
            while not controller.done:
                chapter = controller.queue_out.get()

                # debug
                # brush.print(controller.queue_out.qsize())
                # brush.print(f'{chapter.no} {chapter.title}')

                # update brush
                brush.value += 1

                prefix = f'[{brush.value}/{brush.total}]'
                brush.desc = f'{prefix} {chapter.url}'

                # get data
                self.db.chapters.insert(chapter)

                # at last remove chapter from pending
                self.db.pending.remove(chapter.url)

                controller.queue_out.task_done()

    def create_epub(self):
        with Loader('Create epub'):
            Epub().create(
                novel=self.db.novel.parse(),
                cover=self.cover_path(),
                volumes={},
                chapters=self.db.chapters.all(),
                save_path=self.db.path.parent
            )

    def open_db(self):
        return NovelData(self.url)

    def cover_path(self):
        return self.db.path.parent / Path('cover.jpg')

    def parse_source(self):
        """
        create source object to which the url belongs to

        :return: source object
        """
        for source in [WuxiaWorldCo, BoxNovel, ReadLightNovel]:
            if source.of(self.url):
                return source()

        raise ValueError(f'"{self.url}" does not belong to any available source')
