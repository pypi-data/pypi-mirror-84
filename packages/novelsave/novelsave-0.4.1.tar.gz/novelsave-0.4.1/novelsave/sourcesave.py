from pathlib import Path

from . import Epub
from .concurrent import ConcurrentActionsController
from .database import NovelData
from .sources import sources
from .template import NovelSaveTemplate
from .tools import StringTools, UiTools
from .ui import Loader


class SourceNovelSave(NovelSaveTemplate):
    def __init__(self, url, directory=None):
        super(SourceNovelSave, self).__init__(url, None, None, directory)

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
        with Loader('Update pending') as brush:
            saved = self.db.chapters.all_basic()
            pending = list(set(chapters).difference(saved))

            brush.desc += f' ({len(pending)})'

            self.db.pending.truncate()
            self.db.pending.put_all(pending)

    def download(self, thread_count=4, limit=None):
        pending = self.db.pending.all()
        if not pending:
            print('[✗] No pending chapters')
            return

        pending.sort(key=lambda c: c.order)

        # limiting number of chapters downloaded
        if limit is not None and limit < len(pending):
            pending = pending[:limit]

        with Loader(f'Populating tasks ({len(pending)})', value=0, total=len(pending)) as brush:

            # initialize controller
            controller = ConcurrentActionsController(thread_count, task=self.task)
            for chapter in pending:
                controller.add(chapter)

            # start downloading
            for chapter in controller.iter():
                # debug
                # brush.print(controller.queue_out.qsize())
                # brush.print(f'{chapter.no} {chapter.title}')

                # update brush
                brush.value += 1
                brush.desc = f'[{brush.value}/{brush.total}] {chapter.url}'

                # get data
                self.db.chapters.insert(chapter)

                # at last remove chapter from pending
                self.db.pending.remove(chapter.url)

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
        # trailing slash adds nothing
        url = self.url.rstrip('/ ')
        folder_name = StringTools.slugify(url.split('/')[-1])
        directory = Path(self.user.directory.get()) / Path(folder_name)

        return NovelData(directory)

    def cover_path(self):
        return self.db.path.parent / Path('cover.jpg')

    def parse_source(self):
        """
        create source object to which the url belongs to

        :return: source object
        """
        for source in sources:
            if source.of(self.url):
                return source()

        raise ValueError(f'"{self.url}" does not belong to any available source')

    def task(self, partialc):
        ch = self.source.chapter(partialc.url)
        ch.index = partialc.index

        return ch
