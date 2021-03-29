from flask import Blueprint, request, render_template, redirect, url_for
import json
import time
import rpyc
import sys

from video_file_organizer.__main__ import run_app
from video_file_organizer.config.config import Config
from video_file_organizer.database import utils as db_utils

while True:
    try:
        conn = rpyc.connect('localhost', 2324)
        break
    except ConnectionRefusedError:
        time.sleep(5)
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        raise
config = Config([])

routes = Blueprint("routes", __name__)


@routes.route('/', methods=['GET'])
def index():
    worker_info = [str(x) for x in conn.root.get_jobs()]
    if len(worker_info) == 0:
        worker_info = None
    unsuccessful_files = db_utils.get_unsuccessful_vfiles()
    return render_template(
        'home.html',
        worker_info=worker_info,
        unsuccessful_files=unsuccessful_files
    )


@routes.route('/toggle_scheduler', methods=['GET'])
def toggle_scheduler():
    if len(conn.root.get_jobs()) > 0:
        conn.root.remove_all_jobs()
    else:
        conn.root.add_job('video_file_organizer.__main__:run_app',
                          trigger='interval',
                          minutes=config.schedule, name='vfo')
    return redirect(url_for('routes.index'))


@routes.route('/view_jobs', methods=['GET'])
def view_jobs():
    return json.dumps([str(x) for x in conn.root.get_jobs()])


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

    run_app(whitelist=data['filename'])

    return data


@routes.route('/now', methods=['GET'])
def now():
    run_app()

    return "Success"
