from budgie.frequency import FREQUENCY_TYPES

from datetime import datetime, timedelta
from scipy.stats import skewnorm


class BudgetEvent:

    def __init__(self, amount, frequency_type, start_date=None,
                 end_date=None, credit=True, stdev=0, skew=0):
        if credit:
            self.amount = amount * -1
        else:
            self.amount = amount

        freq = FREQUENCY_TYPES[frequency_type](start_date, end_date)
        self.event_dates = freq.generate_event_dates()
        self.stdev = stdev
        self.skew = skew

        self.data = None
        self.generate_data()

    def generate_event_amount(self):
        return skewnorm.rvs(self.skew, loc=self.amount, scale=self.stdev)

    def generate_run(self):
        run = []
        running_amount = 0
        for i in range(365):
            the_date = (datetime.today() + timedelta(days=i)).date()
            if the_date in self.event_dates:
                new_amount = self.generate_event_amount()
                running_amount = running_amount + new_amount

            run.append(running_amount)

        return run

    def generate_data(self):
        if not self.data:
            data = []
            # TODO: clean this up
            if self.stdev:
                for i in range(100):
                    data.append(self.generate_run())

            else:
                run = self.generate_run()
                for i in range(100):
                    data.append(run)
            self.data = data

        return self.data
