"""Main flask app server"""
import os
from budget_builder.budget_simulator import BudgetSimulator
from flask_app.yaml_loader import no_duplicates_constructor
from flask import (flash, Blueprint, request, make_response,
                   redirect, render_template)
from werkzeug.utils import secure_filename
from string import digits
import datetime  # pylint: disable=unused-import
import yaml

# silence pyflakes -
# https://stackoverflow.com/questions/5033727/how-do-i-get-pyflakes-to-ignore-a-statement/12121404#12121404
assert datetime

financier_app = Blueprint('financier_app', __name__, template_folder='templates')
yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                     no_duplicates_constructor)


def extract_float(value):
    """convert a string into a float. If no value is passed, return 0"""
    # pylint: disable=bare-except

    new_val = str(value or 0)
    try:
        return float(''.join([d for d in new_val if d in digits or d == '.']))
    except:
        return 0


def float_to_currency(value):
    """convert a float to a currency"""
    return "$%.2f" % extract_float(str(value))


def start_balance(req):
    """Get the starting balance from the request"""
    return extract_float(req.cookies.get('start_balance'))


def build_budget(req):
    """Send the 'current_budget' cookie config to the BudgetSimulator"""
    # pylint: disable=eval-used
    # TODO: figure out a better solution than eval
    current_budget = req.cookies.get('current_budget')

    if current_budget:
        return BudgetSimulator(eval(current_budget),
                               start_balance=start_balance(req))


@financier_app.route('/')
def show_budget_simulation():
    """Home page. Show a budget if there is one"""
    simulated_budget = build_budget(request)
    if simulated_budget:
        budget = simulated_budget.budget()
        notes = simulated_budget.notes()
        json_data = simulated_budget.to_json()
    else:
        budget = []
        notes = ['No Budget Supplied. Please upload one']
        json_data = ""
    return render_template('pages/index.html',
                           budget=[i for i in budget],
                           json_data=json_data,
                           notes=notes,
                           start_balance=float_to_currency(start_balance(request)))


@financier_app.route('/upload', methods=['POST'])
def upload_file():
    """Take a yaml file and set it as the current_budget cookie"""
    # pylint: disable=bare-except
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
        if file:
            resp = make_response(redirect('/'))
            filename = secure_filename(file.filename)
            tmp_path = os.path.join('/tmp', filename)
            file.save(tmp_path)
            try:
                budget = str(yaml.load(open(tmp_path, 'r')))
            except:
                # flash("{} is not valid yaml".format(filename))
                os.remove(tmp_path)
                return resp

            resp.set_cookie('current_budget', budget)
            os.remove(tmp_path)
            return resp


@financier_app.route('/set_start_balance', methods=['POST'])
def set_start_balance():
    """Update the 'start_balance' cookie"""
    resp = make_response(redirect('/'))
    resp.set_cookie('start_balance', request.values['start_balance'] or 0)
    return resp


@financier_app.route('/edit_budget')
def edit_budget():
    """Page for displaying/editing the budget events"""
    simulated_budget = build_budget(request)
    return render_template('pages/edit_budget.html',
                           events=simulated_budget.budget_events)
