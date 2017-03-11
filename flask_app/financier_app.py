import os
from datetime import datetime, date, timedelta
from financier import BudgetSimulator
from flask import Blueprint, request, redirect, url_for, render_template, abort
from werkzeug.utils import secure_filename
from jinja2 import TemplateNotFound


financier_app = Blueprint('financier_app', __name__,
                                template_folder='templates')

STORAGE_DIRECTORY = '/financier_data'
WORKING_DIRECTORY = '/tmp/financier_working_dir'
WORKING_FILEPATH = os.path.join(WORKING_DIRECTORY, 'budget.yaml')
ALLOWED_EXTENSIONS = set(['yaml'])

def create_folders():
    for folder in [STORAGE_DIRECTORY, WORKING_DIRECTORY]:
        try:
            os.mkdir(folder)
        except:
            pass
    
# todo
# - change modes (summary vs pretty)
# - show costs/inputs in fields
#     - make updatable
# - export csv
# - save/load config


def get_saved_files():
    files = [f for f in os.listdir(STORAGE_DIRECTORY) if '.yaml' in f]
    return [{'filename': f,
            'full_filename': os.path.join(STORAGE_DIRECTORY, f), 
            'last_modified_at': datetime.strftime(datetime.utcfromtimestamp(os.stat(os.path.join(STORAGE_DIRECTORY, f)).st_ctime),'%Y/%m/%d %H:%M')}
            for f in files]


@financier_app.route('/')
def hello_world():
    create_folders()
    # try:
    budget_simulator = BudgetSimulator(config=WORKING_FILEPATH,
                                        start_balance = 26042)
    budget = budget_simulator.budget()
    return render_template('pages/index.html',
                            budget=[i for i in budget],
                            saved_files = get_saved_files())
    # except:
    #     return abort(404)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def transfer_saved_file_to_working_path(filename):
    with open(os.path.join(STORAGE_DIRECTORY, filename), 'r') as saved_file:
        with open(WORKING_FILEPATH, 'w') as f:
            f.write(saved_file.read())


@financier_app.route('/upload', methods=['POST'])
def upload_file():
    create_folders()
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
            file.save(os.path.join(STORAGE_DIRECTORY, filename))
            transfer_saved_file_to_working_path(filename)
            return redirect('/')

@financier_app.route('/load', methods=['POST'])
def load_file():
    create_folders()
    if request.method == 'POST':
        # print(dir(request))
        file = request.values['file'].split('/')[-1]
        if file and allowed_file(file):
            transfer_saved_file_to_working_path(file)
            return redirect('/')
    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form action="" method=post enctype=multipart/form-data>
    #   <p><input type=file name=file>
    #      <input type=submit value=Upload>
    # </form>
    # '''
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
