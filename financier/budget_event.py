from datetime import date, timedelta


class BudgetEvent(object):

    def __init__(self, name, amount, kind, start_date = None, example_date = date.today(), exact_date = date.today(), end_date = None, day_of_month = None):
        self.name = name
        self.amount = amount
        self.kind = kind
        self.day_of_month = day_of_month
        self.start_date = start_date
        self.example_date = example_date
        self.exact_date = exact_date
        self.end_date = end_date

    def should_update(self, thedate):
        if self.kind == 'one_time': return thedate == self.exact_date
        if (self.start_date and thedate < self.start_date) or (self.end_date and thedate > self.end_date): return False
        #TODO: deal with end of month
        if self.kind == 'monthly': return thedate.day == self.day_of_month
        if self.kind == 'biweekly': return (thedate - self.example_date).days % 14 == 0
        if self.kind == 'bimonthly': return (thedate.day == 15 or thedate.day == 1)

    def update_balance(self, orig_balance, thedate):
        if self.should_update(thedate):
            return thedate, self.name, self.amount, orig_balance + self.amount

    def __repr__(self):
        return "{}(name={}, amount={}, kind={}, start_date={}, end_date={}, day_of_month={})".format(
                self.__class__.__name__,
                self.name,
                self.amount,
                self.kind,
                self.start_date,
                self.end_date,
                self.day_of_month)

