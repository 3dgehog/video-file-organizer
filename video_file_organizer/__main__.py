import logging
import os
import argparse
import sys

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor

from video_file_organizer.app import App


def parse_args(args):
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
    parser.add_argument('--series-rule', action='append', nargs='+', type=str,
                        metavar=('serie', 'rules'))
    # Logging Parameters
    parser.add_argument('-v', '--verbose', action='store_true')
    # ToolKit
    parser.add_argument('--create-config', action='store_true')
    parser.add_argument('--scheduler', action='store_true')
    return parser.parse_args(args)


def setup_logging(args):
    # Setup Logger
    logger = logging.getLogger('vfo')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('vfo.log')
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    # Set log level based on input arguments
    if os.environ.get('LOG') == "DEBUG" or args.verbose:
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

    if os.environ.get('LOG') == "DEBUG" or args.verbose:
        logger.info("Running in verbose mode")


def toolkit(args):
    if args.create_config:
        from video_file_organizer.config import Config, RuleBook
        Config.create_file_from_template()
        RuleBook.create_file_from_template()
        sys.exit(0)

    if args.scheduler:
        executors = {
            'default': ThreadPoolExecutor(1)
        }
        scheduler = BlockingScheduler(executors=executors)
        scheduler.add_job(lambda: run_app(args), 'interval', minutes=1)
        scheduler.start()
        sys.exit(0)


def main():
    args = parse_args(sys.argv[1:])

    setup_logging(args)
    toolkit(args)
    run_app(args)


def run_app(args):
    # App Setup
    app = App()
    app.setup(args)

    # App run
    app.run()


if __name__ == "__main__":
    main()
