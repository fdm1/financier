from financier.budget_simulator import BudgetSimulator
from datetime import datetime, date, timedelta
import pandas as pd
import os
import argparse

def main(params):

    for d in ['start_date', 'end_date']:
        if isinstance(params[d], str):
            params[d] = datetime.strptime(params[d], '%Y-%m-%d').date()
    budget_simulator = BudgetSimulator(config = params['config'],
                                        start_date = params.get('start_date'),
                                        end_date = params.get('end_date'),
                                        start_balance = float(params.get('balance')))


    if params.get('to_csv') != 'False':
        csv_path = params.get('filename')
        if not csv_path:
            csv_path =  params['config'].split('.')[0] + datetime.now().strftime('_%Y%m%d_%H%M') + '.csv'
        budget_simulator.to_csv('/config/{}'.format(os.path.basename(csv_path)), params.get('output'))
    else:
        df = budget_simulator.to_df(params.get('output'))
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_rows', len(df))
        print(df)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate budget forecast')
    parser.add_argument('--config', '-c', default = None, help = 'The location of the config file')
    parser.add_argument('--start_date', '-s', default = date.today(), help = 'Start date (default today)')
    parser.add_argument('--end_date', '-e', default = date.today() + timedelta(365), help = 'End date (default 1 year from today)')
    parser.add_argument('--balance', '-b', default = 0, help = 'Starting balance (default 0)')
    parser.add_argument('--filename', '-f', help = 'filename to output csv to')
    parser.add_argument('--to_csv', default = 'False', help = "generate a csv")
    parser.add_argument('--output', '-o', default = None, help = "output style (summary == only EOM, simple == no pretty print or summary")
    args = parser.parse_args()

    main(vars(args))


