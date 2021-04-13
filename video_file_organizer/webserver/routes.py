from flask import Blueprint, render_template, redirect, url_for
import json

from video_file_organizer.config.config import Config
from video_file_organizer.database import utils as db_utils
from video_file_organizer.webserver.rpyc_client import RPYCClient

rpyc_client = RPYCClient()
conn = None
config = Config([])

routes = Blueprint("routes", __name__)


@routes.route('/', methods=['GET'])
def index():
    global conn
    if not conn:
        conn = rpyc_client.conn
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
    global conn
    if not conn:
        conn = rpyc_client.conn
    if len(conn.root.get_jobs()) > 0:
        conn.root.remove_all_jobs()
    else:
        conn.root.add_job('video_file_organizer.manager:manager.start',
                          trigger='interval',
                          minutes=config.schedule, name='vfo')
    return redirect(url_for('routes.index'))


@routes.route('/view_jobs', methods=['GET'])
def view_jobs():
    global conn
    if not conn:
        conn = rpyc_client.conn
    return json.dumps([str(x) for x in conn.root.get_jobs()])
