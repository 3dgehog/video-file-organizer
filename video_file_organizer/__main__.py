# import logging
import argparse

from video_file_organizer.configs.config_handler import ConfigHandler
# from video_file_organizer.scanners import scan_input_dir, scan_series_dirs


def main():
    # Arguments
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    # Configs
    config = ConfigHandler()
    config.args = args

    # Scanner results
    # fse_queue = scan_input_dir(config)
    # series_index = scan_series_dirs(config)


if __name__ == "__main__":
    main()
