from financier.budget_event import BudgetEvent
from financier.ledger_entry import LedgerEntry
from datetime import date, timedelta
import json


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
            new_event = BudgetEvent(name=e, **self.budget_dict["budget_events"][e])
            budget_events.append(new_event)

        return budget_events

    def ordered_events(self):
        """Return non-one-time events in order of date,
        followed by one-time events ordered by date.

        Used for `edit_budget` view"""

        ordered_events = []
        # today = datetime.today
        # if today.day == 1:
        #     start_month = today.month
        # else:
        #     start_month = today.month + 1
        #
        # start_date = datetime(today.year, start_month, today.day)
        return ordered_events

    def notes(self):
        notes = [
                'Start Date: {}'.format(date.today()),
                'Start Balance: {}'.format("$%.2f" % self.start_balance),
                ]

        if 'notes' in self.budget_dict:
            for note in self.budget_dict['notes']:
                notes.append(note)

        return notes

    @property
    def budget_events(self):
        return self.build_budget_events()

    def simulate_budget(self, sep=','):
        thedate = self.start_date
        balance = self.start_balance
        ledger = [LedgerEntry(thedate=self.start_date,
                              debit_amount=None,
                              credit_amount=None,
                              event="Starting Balance",
                              balance=self.start_balance,
                              sep=sep)]
        min_balance = self.start_balance
        total_min_balance = self.start_balance
        max_balance = self.start_balance
        total_max_balance = self.start_balance
        while thedate <= self.end_date:
            for e in self.budget_events:
                event, thedate, new_balance = e.update_balance(balance, thedate)
                if new_balance:
                    balance = new_balance
                    le = LedgerEntry(event,
                                     thedate=thedate,
                                     balance=balance)
                    ledger.append(le)
                    if balance > total_max_balance:
                        total_max_balance = balance
                    if balance < total_min_balance:
                        total_min_balance = balance
                    if balance > max_balance:
                        max_balance = balance
                    if balance < min_balance:
                        min_balance = balance
            if (thedate + timedelta(1)).day == 1:
                ledger.append(
                    LedgerEntry(thedate=thedate,
                                event="End of Month",
                                debit_amount=None,
                                credit_amount=None,
                                balance=balance,
                                min_balance=min_balance,
                                max_balance=max_balance))
                min_balance = balance
                max_balance = balance
            thedate = thedate + timedelta(1)
        event = LedgerEntry(thedate=self.end_date,
                            event="Ending Balance",
                            debit_amount=None,
                            credit_amount=None,
                            balance=balance,
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
                          not (i.thedate == i.event == i.balance) and
                          i.event not in ('Starting Balance',
                                          'End of Month',
                                          'Ending Balance')
                          )
                      ]
        elif output == 'summary':
            budget = [i for i in budget
                      if i.event in ('Starting Balance',
                                     'End of Month',
                                     'Ending Balance')]
        return budget

    def to_json(self):
        return json.dumps([r.to_json for r in self.budget()][1:])
