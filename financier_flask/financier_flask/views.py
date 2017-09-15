"""Main flask app server"""
import os
from financier_flask.utils.yaml_loader import no_duplicates_constructor
from financier_flask.utils.view_helpers import (
    float_to_currency, start_balance, build_budget
)
from flask import (flash, Blueprint, request, make_response,
                   session, redirect, render_template)
from werkzeug.utils import secure_filename
import yaml

bp = Blueprint('views', __name__, template_folder='templates')
yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                     no_duplicates_constructor)


@bp.route('/')
def show_budget_simulation():
    """Home page. Show a budget if there is one"""
    simulated_budget = build_budget()
    flash('hi')
    if simulated_budget:
        budget = simulated_budget.budget()
        notes = simulated_budget.notes()
        json_data = simulated_budget.to_json()
    else:
        budget = []
        notes = ['No Budget Supplied. Please upload one']
        json_data = ""
    return render_template('index.html',
                           budget=[i for i in budget],
                           json_data=json_data,
                           notes=notes,
                           start_balance=float_to_currency(start_balance()))


@bp.route('/upload', methods=['POST'])
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

            session['current_budget'] = budget
            os.remove(tmp_path)
            return resp


@bp.route('/set_start_balance', methods=['POST'])
def set_start_balance():
    """Update the 'start_balance' cookie"""
    session['start_balance'] = request.values['start_balance'] or 0
    return redirect('/')


@bp.route('/edit_budget')
def edit_budget():
    """Page for displaying/editing the budget events"""
    simulated_budget = build_budget()
    return render_template('pages/edit_budget.html',
                           events=simulated_budget.budget_events)
