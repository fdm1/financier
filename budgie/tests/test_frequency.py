from budgie.frequency import FREQUENCY_TYPES

from datetime import date
import pytest


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

    def test_generate_event_dates_end_date(self):
        start_date = date(2019, 12, 1)
        end_date = date(2019, 12, 16)
        freq = FREQUENCY_TYPES['BiWeekly'](start_date=start_date, end_date=end_date)
        expected_dates = [
            date(2019, 12, 1),
            date(2019, 12, 15),
        ]

        assert set(freq.generate_event_dates()) == set(expected_dates)


class TestMonthly:

    def test_generate_event_dates(self):
        start_date = date(2019, 8, 3)
        freq = FREQUENCY_TYPES['Monthly'](start_date=start_date)
        expected_dates = [
            date(2019, 8, 3),
            date(2019, 9, 3),
            date(2019, 10, 3),
            date(2019, 11, 3),
            date(2019, 12, 3),
        ]

        assert set(freq.generate_event_dates()) == set(expected_dates)

    def test_value_error_after_28th(self):
        start_date = date(2019, 8, 29)
        freq = FREQUENCY_TYPES['Monthly'](start_date=start_date)
        with pytest.raises(ValueError):
            freq.generate_event_dates()
