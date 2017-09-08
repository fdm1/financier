"""A line item of a budget"""


def _to_currency(amount):
    """Format an amount as a currency. If the amount is a string, noop"""
    # pylint: disable=bare-except
    if isinstance(amount, str):
        return amount

    res = amount if amount != 0 else None
    try:
        return ("$%.2f" % round(res, 2)).replace('-', '')
    except:
        return ''


class LedgerEntry(object):
    """An object to represent a line item.
    This can also be strings to hackily create headers and line breaks"""

    def __init__(self, event, debit_amount=None, credit_amount=None,
                 thedate=None, balance=None, min_balance=None,
                 max_balance=None, sep=','):
        # pylint: disable=too-many-arguments

        self.thedate = thedate

        if isinstance(event, str):
            self.debit_amount = debit_amount
            self.credit_amount = credit_amount
            self.event = event
        else:
            self.event = event.name
            self.debit_amount = event.debit_amount
            self.credit_amount = event.credit_amount

        self.balance = balance
        self.min_balance = min_balance
        self.max_balance = max_balance
        self.sep = sep

    # TODO: refactor the stuff below
    # TODO: remove string entry hackery (headers and stuff)

    @property
    def debit_amount_currency(self):
        """currency-formatted debit amount"""
        return _to_currency(self.debit_amount)

    @property
    def credit_amount_currency(self):
        """currency-formatted credit amount"""
        return _to_currency(self.credit_amount)

    @property
    def balance_currency(self):
        """currency-formatted balance"""
        return _to_currency(self.balance)

    @property
    def min_balance_currency(self):
        """currency-formatted min"""
        return _to_currency(self.min_balance)

    @property
    def max_balance_currency(self):
        """currency-formatted max"""
        return _to_currency(self.max_balance)

    def __iter__(self):
        for i in [str(self.thedate),
                  str(self.event),
                  self.debit_amount_currency,
                  self.credit_amount_currency,
                  self.balance_currency,
                  self.min_balance_currency,
                  self.max_balance_currency]:
            yield i

    @property
    def csv_string(self):
        """Return a csv line of thedate and balance"""
        data = [str(self.thedate).lower(),
                str(self.balance).lower()]
        return ','.join(data)

    @property
    def to_json(self):
        """Return a json blob of thedate and balance"""
        return {'date': str(self.thedate), 'balance': str(self.balance)}

    def __str__(self):
        return self.sep.join(list(self))
