from budgie.frequency import FREQUENCY_TYPES

from collections import namedtuple
from datetime import datetime, timedelta
from scipy.stats import skewnorm
from statistics import mean


Event = namedtuple('Event', 'event_date event_amounts')
EventSummary = namedtuple('EventSummary', 'event_date min mean max')

DAYS_PER_YEAR = 365
DEFAULT_SAMPLES = 100


class BudgetEvent:

    def __init__(self, name, amount, frequency_type, start_date=None,
                 end_date=None, credit=True, stdev=0, skew=0,
                 run_days=DAYS_PER_YEAR, samples=DEFAULT_SAMPLES):

        self.name = name
        self._set_amount(amount, credit)
        self.run_days = run_days
        self._set_event_dates(frequency_type, start_date, end_date)
        self.stdev = stdev
        self.skew = skew
        self._set_sample_size(samples)

        self.data = None
        self.summary = None
        self.generate_data()
        self.generate_summary_data()

    def _set_amount(self, amount, credit):
        if credit:
            self.amount = amount * -1
        else:
            self.amount = amount

    def _set_event_dates(self, frequency_type, start_date, end_date):
        if frequency_type not in FREQUENCY_TYPES:
            known_types = ', '.join(FREQUENCY_TYPES.keys())
            raise ValueError(f'"{frequency_type}" is not a known frequency type: ({known_types})')

        freq = FREQUENCY_TYPES[frequency_type](start_date, end_date)
        self.event_dates = freq.generate_event_dates()

    def _set_sample_size(self, samples):
        if self.stdev:
            self.samples = samples
        else:
            self.samples = 1

    def generate_event_amount(self):
        return skewnorm.rvs(self.skew, loc=self.amount, scale=self.stdev)

    def generate_data(self):
        if not self.data:
            data = []
            for i in range(self.run_days):
                event_date = (datetime.today() + timedelta(days=i)).date()
                if event_date in self.event_dates:
                    data.append(Event(event_date, self.generate_event_data()))

            self.data = data

    def generate_event_data(self):
        return [self.generate_event_amount() for i in range(self.samples)]

    def generate_summary_data(self):
        if not self.summary:
            summary = []
            for event in self.data:
                # TODO: maybe flip min/max if credit?
                summary.append(
                    EventSummary(
                        event.event_date,
                        min(event.event_amounts),
                        mean(event.event_amounts),
                        max(event.event_amounts)
                    )
                )

        self.summary = summary
