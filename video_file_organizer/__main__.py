import argparse
import logging

from video_file_organizer.app import App


def main():
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        help="Displays debug messages",
                        action="store_true")
    args = parser.parse_args()

    # Setup Logger
    logger = logging.getLogger('app')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    # Set log level based on input arguments
    if args.verbose:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s:%(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    app = App(args)
    app.setup()
    app.run()


if __name__ == "__main__":
    main()
