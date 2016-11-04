import os
from datetime import datetime, date, timedelta
from financier import BudgetSimulator
from flask import Blueprint, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from jinja2 import TemplateNotFound


financier_app = Blueprint('financier_app', __name__,
                                template_folder='templates')

UPLOAD_FOLDER = '/tmp/configs'
ALLOWED_EXTENSIONS = set(['yaml'])


# todo
# - change modes (summary vs pretty)
# - show costs/inputs in fields
#     - make updatable
# - export csv
# - DOCKERFILE - mkdir UPLOAD_FOLDER
# - save/load config

# @financier_app.route('/', defaults={'page': 'index'})

# @financier_app.route('/<page>')
# def show(page):
#     try:
#         return render_template('pages/%s.html' % page)
#     except TemplateNotFound:
#         abort(404)

@financier_app.route('/')
def hello_world():
    try:
        budget_simulator = BudgetSimulator(config='{}/budget.yaml'.format(UPLOAD_FOLDER),
                                            start_balance = 100)
                                            # start_balance = 7271)
        budget = budget_simulator.budget()
        return render_template('pages/index.html', budget=[i for i in budget])
    # except Exception, e:
    #     raise e
    except FileNotFoundError:
        return redirect('/upload')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@financier_app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, 'budget.yaml'))
            return redirect('/')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
#
# @app.route('/events')
# def get_routes():
#     try:
#         budget_simulator = BudgetSimulator(config='{}/budget.yaml'.format(UPLOAD_FOLDER),
#                                             start_balance = 6000)
#     except:
#         os.mkdir(UPLOAD_FOLDER)
#         return redirect('/upload')
#     return str(budget_simulator.budget_events)
#
