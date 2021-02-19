from flask import Blueprint, request, render_template, redirect, url_for
import json

from apscheduler.schedulers.background import BackgroundScheduler

from video_file_organizer.__main__ import run_app
from video_file_organizer.config.config import Config
from video_file_organizer.database import utils as db_utils


scheduler = BackgroundScheduler()
scheduler.start()

config = Config([])

scheduler.add_job(
    run_app, trigger='interval', minutes=config.schedule, name='vfo')

routes = Blueprint("routes", __name__)


@routes.route('/', methods=['GET'])
def index():
    worker_info = [str(x) for x in scheduler.get_jobs()]
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
    if len(scheduler.get_jobs()) > 0:
        scheduler.remove_all_jobs()
    else:
        scheduler.add_job(run_app, trigger='interval',
                          minutes=config.schedule, name='vfo')
    return redirect(url_for('routes.index'))


@routes.route('/view_jobs', methods=['GET'])
def view_jobs():
    return json.dumps([str(x) for x in scheduler.get_jobs()])


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
