from abc import ABC
from datetime import date, datetime, timedelta

FREQUENCY_TYPES = dict()


def frequency(klass):
    FREQUENCY_TYPES[klass.__name__] = klass
    return klass


class Frequency(ABC):

    def __init__(self, start_date=None, end_date=None):
        if start_date:
            if isinstance(start_date, date):
                start_date = datetime(start_date.year, start_date.month, start_date.day)
            self.start_date = start_date
        else:
            self.start_date = datetime.today()

        if end_date:
            if isinstance(end_date, date):
                end_date = datetime(end_date.year, end_date.month, end_date.day)
            self.end_date = end_date
        else:
            self.end_date = datetime.today() + timedelta(days=1000)

    def generate_event_dates(self):
        pass


@frequency
class OneTime(Frequency):

    def generate_event_dates(self):
        return [self.start_date.date()]


@frequency
class BiWeekly(Frequency):

    def generate_event_dates(self):
        days = []
        today = datetime.today()
        for i in range(365):
            date = today + timedelta(days=i)
            if (abs((date - self.start_date).days) % 14 == 0 and
                    date >= self.start_date and
                    date <= self.end_date):

                days.append(date.date())

        return days
