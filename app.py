
from flask import Flask
from flask_app.financier_app import financier_app

app = Flask(__name__)
app.register_blueprint(financier_app)
# Blueprint can be registered many times
app.register_blueprint(financier_app, url_prefix='/pages')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
