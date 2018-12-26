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
    args = parser.parse_args()

    # Setup Logger
    logger = logging.getLogger('app')
    # LFRI = Log File Relevent Information
    logging.addLevelName(11, 'LFRI')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('vfo.log')
    fh.setLevel(11)

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

    if args.config:
        app = App(config_dir=args.config[0], args=args)
        logger.info("Running custom configs in {}".format(args.config[0]))
    else:
        app = App(args=args)
    app.setup()
    app.run()


if __name__ == "__main__":
    main()
