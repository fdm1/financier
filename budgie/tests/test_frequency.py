from budgie.frequency import FREQUENCY_TYPES

from datetime import date
from freezegun import freeze_time
import pytest


@pytest.fixture(autouse=True)
def set_date():
    with freeze_time("2019-01-01"):
        yield


class TestOneTime:

    def test_generate_event_dates(self):
        start_date = date(2019, 10, 11)
        freq = FREQUENCY_TYPES['OneTime'](start_date=start_date)
        assert freq.generate_event_dates() == [start_date]


class TestBiWeekly:

    def test_generate_event_dates(self):
        start_date = date(2019, 12, 1)
        freq = FREQUENCY_TYPES['BiWeekly'](start_date=start_date)
        expected_dates = [
            date(2019, 12, 1),
            date(2019, 12, 15),
            date(2019, 12, 29),
        ]

        assert set(freq.generate_event_dates()) == set(expected_dates)
