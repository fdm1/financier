import locale

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

class LedgerEntry(object):
    def __init__(self, thedate, event, debit_amount=None, credit_amount=None, balance=None, min_balance = None, max_balance = None, sep = ','):
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
                res = ''
            else:
                res = amount
            if isinstance(res, str):
                return res
            return locale.currency(res)
        except:
            return ''

    @property
    def debit_amount_currency(self):
        return self._to_currency(self.debit_amount)

    @property
    def credit_amount_currency(self):
        return self._to_currency(self.credit_amount)

    @property
    def balance_currency(self):
        return self._to_currency(self.balance)

    @property
    def min_balance_currency(self):
        return self._to_currency(self.min_balance)

    @property
    def max_balance_currency(self):
        return self._to_currency(self.max_balance)

    def __iter__(self):
        for i in [str(self.thedate),
               str(self.event),
               self.debit_amount_currency,
               self.credit_amount_currency,
               self.balance_currency,
               self.min_balance_currency,
               self.max_balance_currency ]:
            yield i


    @property
    def csv_string(self):
        data = [str(self.thedate).lower(),
                # str(self.event).lower(),
                str(self.balance).lower()
               ]
        return ','.join(data)



    def __str__(self):
        return self.sep.join(list(self))

# class LineBreak(LedgerEntry):
#     def __init__(self, filler = '----', sep = ',', **kwargs):
#         self.thedate =          kwargs.get('thedate') or filler
#         self.event =            kwargs.get('event') or filler
#         self.debit_amount =     kwargs.get('debit_amount') or filler
#         self.credit_amount =    kwargs.get('credit_amount') or filler
#         self.balance =          kwargs.get('balance') or filler
#         self.min_balance =      kwargs.get('min_balance') or filler
#         self.max_balance =      kwargs.get('max_balance') or filler
#         self.sep = sep
