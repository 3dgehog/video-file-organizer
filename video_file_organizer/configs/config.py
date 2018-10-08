import os

CONFIG_DIR = os.path.join(os.environ['HOME'], '.config/video_file_organizer/')
CONFIG_TEMPLATES = os.path.join(os.path.dirname(__file__), 'config_templates')
VIDEO_EXTENSIONS = ['mkv', 'm4v', 'avi', 'mp4', 'mov']