import os
import datetime
from financier import BudgetSimulator
from flask_app.yaml_loader import no_duplicates_constructor
from flask import flash, Blueprint, request, make_response, redirect, url_for, render_template, abort
from werkzeug.utils import secure_filename
from jinja2 import TemplateNotFound
import yaml


financier_app = Blueprint('financier_app', __name__, template_folder='templates')
yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                     no_duplicates_constructor)

ALLOWED_EXTENSIONS = set(['yaml'])

# todo
# - change modes (summary vs pretty)
# - show costs/inputs in fields
#     - make updatable
# - export csv
# - save/load config



@financier_app.route('/')
def show_budget():
    start_balance = float(request.cookies.get('start_balance') or 0)
    current_budget = request.cookies.get('current_budget')
    if current_budget and isinstance(eval(current_budget), dict):
        budget_simulator = BudgetSimulator(eval(current_budget),
                                           start_balance=start_balance)
        budget = budget_simulator.budget()
        notes = budget_simulator.notes()
        json_data = budget_simulator.to_json()
    else:
        budget = []
        notes = ['No Budget Supplied. Please upload one']
        json_data=""
    return render_template('pages/index.html',
                            budget=[i for i in budget],
                            json_data=json_data,
                            notes=notes)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@financier_app.route('/upload', methods=['POST'])
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
            tmp_path = os.path.join('/tmp', filename)
            file.save(tmp_path)
            resp = make_response(redirect('/'))
            resp.set_cookie('current_budget', str(yaml.load(open(tmp_path, 'r'))))
            os.remove(tmp_path)
            return resp


@financier_app.route('/set_start_balance', methods=['POST'])
def set_start_balance():
    resp = make_response(redirect('/'))
    resp.set_cookie('start_balance', str(request.values['start_balance']) or 0)
    return resp
