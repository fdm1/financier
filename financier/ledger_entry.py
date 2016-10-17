import locale

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

class LedgerEntry(object):
    def __init__(self, thedate, event, debit_amount, credit_amount, balance, min_balance = None, max_balance = None, sep = ','):
        self.thedate = thedate
        self.event = event
        self.debit_amount = debit_amount
        self.credit_amount = credit_amount
        self.balance = balance
        self.min_balance = min_balance
        self.max_balance = max_balance
        self.sep = sep

    def _to_currency(self, amount):
        try:
            if amount == 0:
                return ''
            return locale.currency(amount)
        except:
            if isinstance(self, LineBreak):
                return str(amount)
            else:
                return ''

    def __str__(self):
        return self.sep.join([str(self.thedate), 
                                str(self.event), 
                                self._to_currency(self.debit_amount), 
                                self._to_currency(self.credit_amount), 
                                self._to_currency(self.balance),
                                self._to_currency(self.min_balance),
                                self._to_currency(self.max_balance) ])

class LineBreak(LedgerEntry):
    def __init__(self, filler = '----', sep = ','):
        self.thedate = filler
        self.event = filler
        self.debit_amount = filler
        self.credit_amount = filler
        self.balance = filler
        self.min_balance = filler
        self.max_balance = filler
        self.sep = sep
