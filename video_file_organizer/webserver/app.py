from flask import Flask

from .routes import routes
from video_file_organizer.database.utils import init_db

app = Flask(__name__)

init_db()
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run("0.0.0.0", 5050, debug=True)
