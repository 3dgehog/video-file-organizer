from video_file_organizer.app import App

from video_file_organizer.handlers.event import EventHandler


def test_success_eventhandler():
    app = App()
    EventHandler(app)
