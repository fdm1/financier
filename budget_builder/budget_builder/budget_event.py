"""Object to represent budget events"""
from datetime import date, datetime


class UnsupportedEventType(Exception):
    """Error for when unknown event types are given"""
    pass


def getdate(val):
    if isinstance(val, (date, datetime)):
        return val
    else:
        return datetime.strptime(val, '%Y-%m-%d')

class BudgetEvent(object):
    """
    An item used to define a recurring or one-time
    budgeting event (e.g. payday, bills, bonuses, trips)
    """

    VALID_EVENT_TYPES = ['one_time', 'monthly', 'biweekly', 'bimonthly']

    def __init__(self, name, amount, kind, start_date=None,
                 example_date=date.today(), exact_date=date.today(),
                 end_date=None, day_of_month=None):
        # pylint: disable=too-many-arguments
        self.name = name

        if kind not in self.VALID_EVENT_TYPES:
            raise UnsupportedEventType("{} kind is not a supported budget event type".format(kind))

        if amount >= 0:
            self.debit_amount = amount
            self.credit_amount = 0
        else:
            self.debit_amount = 0
            self.credit_amount = amount
        self.kind = kind
        self.day_of_month = day_of_month
        self.start_date = getdate(start_date)
        self.example_date = getdate(example_date)
        self.exact_date = getdate(exact_date)
        self.end_date = getdate(end_date)

    @property
    def debit(self):
        """Return boolean True if this is a debit"""
        return self.debit_amount > 0 and self.credit_amount == 0

    def should_update(self, thedate):
        """Determine if the event has any effect on a given date"""
        if self.kind == 'one_time':
            return thedate == self.exact_date
        elif ((self.start_date and thedate < self.start_date) or
              (self.end_date and thedate > self.end_date)):
            return False
        # TODO: deal with end of month
        elif self.kind == 'monthly':
            return thedate.day == self.day_of_month
        elif self.kind == 'biweekly':
            return (thedate - self.example_date).days % 14 == 0
        elif self.kind == 'bimonthly':
            return thedate.day == 15 or thedate.day == 1

        return False

    def update_balance(self, orig_balance, thedate):
        """Update a balance with the event's amount if needed"""
        balance = None

        if self.should_update(thedate):
            balance = orig_balance + self.debit_amount + self.credit_amount

        return self, thedate, balance

    def __repr__(self):
        return ("{}(name={}, debit_amount={}, credit_amount = {}, "
                "kind={}, start_date={}, end_date={}, day_of_month={})".format(
                    self.__class__.__name__,
                    self.name,
                    self.debit_amount,
                    self.credit_amount,
                    self.kind,
                    self.start_date,
                    self.end_date,
                    self.day_of_month))
