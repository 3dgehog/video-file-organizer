import argparse
import logging

from video_file_organizer.app import App


def main():
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        help="Displays debug messages",
                        action="store_true")
    parser.add_argument("-c", "--config",
                        help="Custom config files location",
                        nargs=1)
    parser.add_argument("--create-config",
                        help="Displays debug messages",
                        action="store_true")
    args = parser.parse_args()

    # Setup Logger
    logger = logging.getLogger('vfo')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('vfo.log')
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    # Set log level based on input arguments
    if args.verbose:
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

    if args.verbose:
        logger.info("Running in verbose mode")

    # App Setup
    app = App()
    kwargs: dict = {}

    if args.config:
        logger.info(f"Running custom configs in {args.config[0]}")
        kwargs.update(config_dir=args.config[0])

    if args.create_config:
        kwargs.update(create=True)

    app.setup(**kwargs)

    # App run
    app.run()


if __name__ == "__main__":
    main()
