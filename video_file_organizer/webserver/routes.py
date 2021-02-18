from flask import Blueprint, request

from video_file_organizer.app import App

routes = Blueprint("routes", __name__)


@routes.route('/', methods=['GET'])
def index():
    return "Video File Orgainzer Webserver is running correctly"


@routes.route('/add_file', methods=['POST'])
def add_file():

    data = request.get_json()

    if data is None:
        return {
            "error": "Make sure your request is in json format or has the \
                correct header for content type 'application/json'"
        }

    if 'filename' not in data:
        return {
            "error": "filename is required"
        }

    vfo = App()
    vfo.setup()
    vfo.run(whitelist=data['filename'])

    return data


@routes.route('/now', methods=['GET'])
def now():
    vfo = App()
    vfo.setup()
    vfo.run()

    return "Success"
