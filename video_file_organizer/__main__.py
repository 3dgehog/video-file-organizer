import argparse

from video_file_organizer.app import App


def main():
    # Arguments
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    app = App(args)
    app.run()


if __name__ == "__main__":
    main()
