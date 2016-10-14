from financier.budget_event import BudgetEvent
from financier.ledger_entry import LedgerEntry, LineBreak
from datetime import date, timedelta
from financier.reqs import yaml
import pandas as pd
import logging


class BudgetSimulator(object):

    def __init__(self, config, start_balance = 0,
                        end_date = date.today() + timedelta(365),
                        start_date = date.today()):
                        
        self.start_balance = start_balance
        self.start_date = start_date
        self.end_date = end_date
        self.config = config

    def __repr__(self):
        return "{}(start_date={}, start_balance={}, end_date={}, config={})".format(
                self.__class__.__name__,
                self.start_date,
                self.start_balance,
                self.end_date,
                self.config)

    def build_budget_events(self):
        budget_events = []
        config = yaml.load(open(self.config, 'r'))
        for e in config["budget_events"]:
            budget_events.append(BudgetEvent(name = e, **config["budget_events"][e]))
        return budget_events

    def simulate_budget(self, sep = ','):
        budget_events = self.build_budget_events()
        thedate = self.start_date
        running_balance = self.start_balance
        line_break = LineBreak(sep = sep)
        empty_line = LineBreak(filler = '', sep = sep)
        ledger = [LedgerEntry(self.start_date, "Starting Balance", None, self.start_balance, sep), line_break]
        while thedate <= self.end_date:
            for e in budget_events:
                event = e.update_balance(running_balance, thedate)
                if event:
                    le = LedgerEntry(*event)
                    ledger.append(le)
                    running_balance = le.balance
            if (thedate + timedelta(1)).day == 1:
                ledger.append(LineBreak())
                ledger.append(LedgerEntry(thedate, "End of Month", None, running_balance))
                ledger.append(empty_line)
            thedate = thedate + timedelta(1)
        ledger.append(empty_line)
        ledger.append(line_break)
        ledger.append(LedgerEntry(self.end_date, "Ending Balance", None, running_balance))
        return ledger

    def __str__(self):
        ledger = self.simulate_budget()
        print("Date\tEvent\tAmount\tBalance")
        for event in ledger:
            print(event)

    def to_df(self):
        df = pd.DataFrame([str(l).split(',') for l in self.simulate_budget()])
        df.columns = ["Date", "Event", "Amount", "Balance"]
        return df

    def to_csv(self, filename):
        df = self.to_df()
        logging.info('Generating budget to {}'.format(filename))
        df[(df.Date != df.Amount) | (df.Date != df.Event) | (df.Date != df.Balance)].to_csv(filename, index = False)




