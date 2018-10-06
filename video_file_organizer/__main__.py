# import logging
import queue
import argparse

from video_file_organizer.config_handler import ConfigHandler
from video_file_organizer.searcher import searcher


def main():
    # Arguments
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    # Configs
    config = ConfigHandler()
    config.args = args

    # Queues
    # match_queue = queue.Queue()
    search_queue = queue.Queue()

    searcher(config, search_queue)


if __name__ == "__main__":
    main()
