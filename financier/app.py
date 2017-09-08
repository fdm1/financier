"""Wrapper to launch the flask app"""

from flask import Flask
from flask_session import Session
from flask_app.financier_app import financier_app

app = Flask(__name__)
app.register_blueprint(financier_app)
# Blueprint can be registered many times
app.register_blueprint(financier_app, url_prefix='/pages')

Session(app)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
