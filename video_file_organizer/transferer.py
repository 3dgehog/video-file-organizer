import shutil
import os
import logging


from video_file_organizer.models import VideoFile

logger = logging.getLogger('vfo.transferer')


class Transferer:
    def __init__(self):
        pass

    def __enter__(self):  # HERE: returning self
        self.delete_list = []
        return self

    def __exit__(self, type, value, traceback):
        # Removes duplicates
        self.delete_list = list(set(self.delete_list))

        for source in self.delete_list:
            try:
                os.remove(source)
            except PermissionError:
                # Getting permission error when its a folder
                shutil.rmtree(source)
            logger.info(f"Deleted {os.path.basename(source)}")

    def transfer_vfile(self, vfile: VideoFile):
        if not isinstance(vfile, VideoFile):
            raise TypeError("vfile needs to be an instance of VideoFile")
        if not hasattr(vfile, 'transfer'):
            raise ValueError("vfile needs to have transfer as an attribute")
        if 'transfer_to' not in vfile.transfer:
            raise KeyError("transfer_to key missing in transfer attribute")

        source = vfile.path
        destination = vfile.transfer['transfer_to']
        root_path = vfile.root_path

        self.transfer(source, destination, root_path)

    def transfer(self, source: str, destination: str, root_path: str):
        self._copy(source, destination)
        self._delete(root_path)

    def _copy(self, source: str, destination: str):
        logger.info(f"Transfering {os.path.basename(source)} to {destination}")
        shutil.copy(source, destination)

    def _delete(self, source: str):
        self.delete_list.append(source)
