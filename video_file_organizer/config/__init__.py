import os
import logging

from typing import Union

logger = logging.getLogger('vfo.config')

DEFAULT_DIR = '.config/video_file_organizer/'


def setup_config_dir(
        path: Union[str, None],
        create: bool = False) -> str:

    if not path:
        path = os.path.join(os.environ['HOME'], DEFAULT_DIR)
        logger.debug(
            f'No config dir path given, going to default path of: {path}')

    if create:
        os.makedirs(path, exist_ok=True)
        logger.info("Config directory created")

    if not os.path.exists(path):
        raise FileNotFoundError("Config directory doesn't exist")

    return path
