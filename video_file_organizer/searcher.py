import logging
import os
import queue

from video_file_organizer.config_handler import ConfigHandler


def searcher(config: ConfigHandler, search_queue: queue.Queue):
    logging.info("Running Searcher")

    for item in os.listdir(config.input_dir):

        # Ignore folders or files from config
        if item in config.ignore_folders or item in config.ignore_files:
            logging.debug("'{}' ignored".format(item))
            continue
