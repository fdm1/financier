# pylint: disable=missing-docstring
from budget_builder.budget_simulator import BudgetSimulator  # pylint: disable=no-name-in-module
from flask import escape, session
from string import digits
import datetime  # pylint: disable=unused-import

# silence pyflakes -
# https://stackoverflow.com/questions/5033727/how-do-i-get-pyflakes-to-ignore-a-statement/12121404#12121404
assert datetime


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


def start_balance():
    """Get the starting balance from the session"""
    balance = escape(session['start_balance']) if 'start_balance' in session else 0
    return extract_float(balance)


def build_budget():
    """Set the 'current_budget' session config to the BudgetSimulator"""
    # pylint: disable=eval-used
    # TODO: figure out a better solution than eval
    if 'current_budget' in session:
        current_budget = session['current_budget']

        return BudgetSimulator(eval(current_budget),
                               start_balance=start_balance())
