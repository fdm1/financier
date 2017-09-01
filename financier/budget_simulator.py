from financier.budget_event import BudgetEvent
from financier.ledger_entry import LedgerEntry
from datetime import date, timedelta
import json
import yaml


class BudgetSimulator(object):

    def __init__(self, budget_dict, start_balance=0, end_date=date.today() + timedelta(365),
                 start_date=date.today()):

        self.start_balance = start_balance
        self.start_date = start_date
        self.end_date = end_date
        self.budget_dict = budget_dict

    def __repr__(self):
        return "{}(start_date={}, start_balance={}, end_date={})".format(
                self.__class__.__name__,
                self.start_date,
                self.start_balance,
                self.end_date)


    def build_budget_events(self):
        budget_events = []
        for e in self.budget_dict["budget_events"]:
            budget_events.append(BudgetEvent(name = e, **self.budget_dict["budget_events"][e]))
        return budget_events

    def notes(self):
        notes = [
                'Start Date: {}'.format(date.today()),
                'Start Balance: {}'.format(self.start_balance),
                ]

        if 'notes' in self.budget_dict:
            for note in self.budget_dict['notes']:
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


    def to_json(self):
        return json.dumps([r.to_json for r in self.budget()][1:])
