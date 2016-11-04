from datetime import date, timedelta


class BudgetEvent(object):


    def __init__(self, name, amount, kind, start_date = None, example_date = date.today(), exact_date = date.today(), end_date = None, day_of_month = None):
        self.name = name
        if amount >= 0:
            self.debit_amount = amount
            self.credit_amount = 0
        else:
            self.debit_amount = 0
            self.credit_amount = amount
        self.kind = kind
        self.day_of_month = day_of_month
        self.start_date = start_date
        self.example_date = example_date
        self.exact_date = exact_date
        self.end_date = end_date

    @property
    def debit(self):
        return self.debit_amount > 0 and self.credit_amount == 0

    def should_update(self, thedate):
        if self.kind == 'one_time': return thedate == self.exact_date
        if (self.start_date and thedate < self.start_date) or (self.end_date and thedate > self.end_date): return False
        #TODO: deal with end of month
        if self.kind == 'monthly': return thedate.day == self.day_of_month
        if self.kind == 'biweekly': return (thedate - self.example_date).days % 14 == 0
        if self.kind == 'bimonthly': return (thedate.day == 15 or thedate.day == 1)
        return False

    def update_balance(self, orig_balance, thedate):
        if self.should_update(thedate):
            return thedate, self.name, self.debit_amount, self.credit_amount, orig_balance + self.debit_amount + self.credit_amount, None, None

    def __repr__(self):
        return "{}(name={}, debit_amount={}, credit_amount = {}, kind={}, start_date={}, end_date={}, day_of_month={})".format(
                self.__class__.__name__,
                self.name,
                self.debit_amount,
                self.credit_amount,
                self.kind,
                self.start_date,
                self.end_date,
                self.day_of_month)

