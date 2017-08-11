from financier.budget_event import BudgetEvent
from financier.ledger_entry import LedgerEntry
from financier.yaml_loader import no_duplicates_constructor
from datetime import date, timedelta
import os
import yaml
# import pandas as pd
import logging


class BudgetSimulator(object):

    def __init__(self, config, start_balance = 0,
                        end_date = date.today() + timedelta(365),
                        start_date = date.today()):

        self.start_balance = start_balance
        self.start_date = start_date
        self.end_date = end_date
        self.config_file = config
        self.config = yaml.load(open(config, 'r'))

    def __repr__(self):
        return "{}(start_date={}, start_balance={}, end_date={}, config={})".format(
                self.__class__.__name__,
                self.start_date,
                self.start_balance,
                self.end_date,
                self.config_file)


    def build_budget_events(self):
        budget_events = []
        yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                                no_duplicates_constructor)
        for e in self.config["budget_events"]:
            budget_events.append(BudgetEvent(name = e, **self.config["budget_events"][e]))
        return budget_events

    def notes(self):
        notes = [
                'Start Date: {}'.format(date.today()),
                'Start Balance: {}'.format(os.getenv('START_BALANCE')),
                ]

        if 'notes' in self.config:
            for note in self.config['notes']:
                notes.append(note)

        return notes


    @property
    def budget_events(self):
        return self.build_budget_events()

    def simulate_budget(self, sep = ','):
        thedate = self.start_date
        running_balance = self.start_balance
        ledger = [LedgerEntry(thedate=self.start_date,
                                debit_amount=None,
                                credit_amount=None,
                                event="Starting Balance",
                                balance=self.start_balance, 
                                sep = sep)]
        min_balance = self.start_balance
        total_min_balance = self.start_balance
        max_balance = self.start_balance
        total_max_balance = self.start_balance
        while thedate <= self.end_date:
            for e in self.budget_events:
                event = e.update_balance(running_balance, thedate)
                if event:
                    le = LedgerEntry(*event)
                    ledger.append(le)
                    running_balance = le.balance
                    if running_balance > total_max_balance:
                        total_max_balance = running_balance
                    if running_balance < total_min_balance:
                        total_min_balance = running_balance
                    if running_balance > max_balance:
                        max_balance = running_balance
                    if running_balance < min_balance:
                        min_balance = running_balance
            if (thedate + timedelta(1)).day == 1:
                ledger.append(
                    LedgerEntry(thedate=thedate,
                                event="End of Month",
                                debit_amount=None,
                                credit_amount=None,
                                balance=running_balance,
                                min_balance=min_balance,
                                max_balance=max_balance))
                min_balance = running_balance
                max_balance = running_balance
            thedate = thedate + timedelta(1)
        event = LedgerEntry(thedate=self.end_date,
                                    event="Ending Balance", 
                                    debit_amount=None,
                                    credit_amount=None,
                                    balance=running_balance, 
                                    min_balance=total_min_balance, 
                                    max_balance=total_max_balance)
        ledger.append(event)
        return ledger

    def budget(self, output=None):
        budget = [LedgerEntry("Date", "Event", "Debit", "Credit",
                                "Balance", "Min", "Max")]
        for l in self.simulate_budget():
            budget.append(l)

        if output == 'simple':
            budget = [i for i in budget if (
                        not (i.thedate == i.event ==i.balance)
                        and i.event not in ('Starting Balance',
                                            'End of Month',
                                            'Ending Balance'))]
        elif output == 'summary':
            budget = [i for i in budget
                    if i.event in ('Starting Balance',
                                    'End of Month',
                                    'Ending Balance')]
        return budget

    def to_csv(self, filename, output=None):
        df = self.to_df(output)
        logging.info('Generating budget to {}'.format(filename))
        df.to_csv(filename, index = False)
