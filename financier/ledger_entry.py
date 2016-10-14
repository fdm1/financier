import locale

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

class LedgerEntry(object):
    def __init__(self, thedate, event, amount, balance, sep = ','):
        self.thedate = thedate
        self.event = event
        self.amount = amount
        self.balance = balance
        self.sep = sep

    def _to_currency(self, amount):
        try:
            return locale.currency(amount)
        except:
            if isinstance(self, LineBreak):
                return str(amount)
            else:
                return ''

    def __str__(self):
        return self.sep.join([str(self.thedate), 
                                str(self.event), 
                                self._to_currency(self.amount), 
                                self._to_currency(self.balance)])

class LineBreak(LedgerEntry):
    def __init__(self, filler = '----', sep = ','):
        self.thedate = filler
        self.event = filler
        self.amount = filler
        self.balance = filler
        self.sep = sep
