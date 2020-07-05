import logging
import os

from video_file_organizer.app import App


def main():
    # Setup Logger
    logger = logging.getLogger('vfo')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('vfo.log')
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    # Set log level based on input arguments
    if os.environ.get('DEBUG'):
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)

    file_format = logging.Formatter(
        '%(asctime)s - %(levelname)s:%(message)s')
    console_format = logging.Formatter(
        '%(message)s')

    ch.setFormatter(console_format)
    fh.setFormatter(file_format)

    logger.addHandler(ch)
    logger.addHandler(fh)

    if os.environ.get('DEBUG'):
        logger.info("Running in verbose mode")

    # App Setup
    app = App()
    kwargs: dict = {}

    if os.environ.get('CONFIG_DIR'):
        logger.info(f"Running custom configs in {os.environ['CONFIG_DIR']}")
        kwargs.update(config_dir=os.environ['CONFIG_DIR'])

    app.setup(**kwargs)

    # App run
    app.run()


if __name__ == "__main__":
    main()
