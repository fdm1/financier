"""Wrapper to launch the flask app"""

import os

from flask import Flask
from flask_session import Session
from financier_flask import views

app = Flask(__name__)
# Blueprint can be registered many times
app.register_blueprint(views.bp)

app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp/flask_sessions'
Session(app)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
