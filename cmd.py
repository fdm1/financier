from financier.budget_simulator import BudgetSimulator
from datetime import datetime, date, timedelta
import pandas as pd
import os
import argparse

def main(params):
    budget_simulator = BudgetSimulator(config = params['config'],
                                        start_date = params.get('start_date'),
                                        end_date = params.get('end_date'),
                                        start_balance = params.get('balance'))


    if params.get('to_csv') == "True":
        filepath = params.get('filename', params['config'].split('/')[-1].split('.')[0] + datetime.now().strftime('_%Y%m%d_%H%M') + '.csv')
        budget_simulator.to_csv(filepath)
    else:
        with pd.option_context('display.max_rows', 999, 'display.max_columns', 5):
            print(budget_simulator.to_df())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate budget forecast')
    parser.add_argument('--config', '-c', default = None, help = 'The location of the config file')
    parser.add_argument('--start_date', '-s', default = date.today(), help = 'Start date (default today)')
    parser.add_argument('--end_date', '-e', default = date.today() + timedelta(365), help = 'End date (default 1 year from today)')
    parser.add_argument('--balance', '-b', default = 0, help = 'Starting balance (default 0)')
    parser.add_argument('--filename', '-f', help = 'filename to output csv to')
    parser.add_argument('--to_csv', default = 'True', help = "generate a csv")
    args = parser.parse_args()

    main(vars(args))


