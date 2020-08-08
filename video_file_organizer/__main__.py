import logging
import os
import argparse

from video_file_organizer.app import App


def main():
    parser = argparse.ArgumentParser()
    # Config Parameters
    parser.add_argument('--config-file', action='store', nargs=1, type=str)
    parser.add_argument('--input-dir', action='store', nargs=1, type=str)
    parser.add_argument('--series-dirs', action='store', nargs='+', type=str)
    parser.add_argument('--ignore', action='store', nargs='+')
    parser.add_argument('--before-scripts', action='store',
                        nargs='+', type=str)
    parser.add_argument('--on-transfer-scripts',
                        action='store', nargs='+', type=str)
    # RuleBook Parameters
    parser.add_argument('--rule-book-file', action='store', nargs=1, type=str)
    parser.add_argument('--series-rule', action='append', nargs=2, type=str,
                        metavar=('serie', 'rules'))
    args = parser.parse_args()

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
    app.setup(args)

    # App run
    app.run()


if __name__ == "__main__":
    main()
