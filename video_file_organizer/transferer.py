import shutil
import os
import logging


from video_file_organizer.entries import VideoFileEntry
from video_file_organizer.utils import Observee
from video_file_organizer.database import Database

logger = logging.getLogger('vfo.transferer')


class Transferer(Observee):
    def __init__(self, database: Database):
        self.database = database

    def __enter__(self):
        Observee.__enter__(self)
        self.delete_list = []
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        Observee.__exit__(self, exc_type, exc_value, exc_traceback)
        # Removes duplicates
        self.delete_list = list(set(self.delete_list))

        for source in self.delete_list:
            if os.path.isfile(source):
                os.remove(source)
            elif os.path.isdir(source):
                shutil.rmtree(source)
            else:
                raise TypeError(f'Unknown type for {source}')
            logger.info(f"Deleted {os.path.basename(source)}")

    def __call__(self, vfile: VideoFileEntry):
        if not isinstance(vfile, VideoFileEntry):
            raise TypeError("vfile needs to be an instance of VideoFileEntry")
        if not hasattr(vfile, 'transfer'):
            raise ValueError("vfile needs to have transfer as an attribute")

        source = vfile.path
        destination = vfile.transfer

        if vfile.depth < 2:
            root_path = vfile.path
        else:
            root_path = os.path.dirname(vfile.path)

        self.transfer(source, destination, root_path)

        self.database.add_successful_vfile(
            vfile.name, vfile.hash, vfile.transfer)

    def transfer(self, source: str, destination: str, root_path: str):
        self._copy(source, destination)
        self._delete(root_path)

    def _copy(self, source: str, destination: str):
        logger.info(f"Transfering {os.path.basename(source)} to {destination}")
        shutil.copy(source, destination)

    def _delete(self, source: str):
        self.delete_list.append(source)
