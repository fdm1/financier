from budgie.budget_event import BudgetEvent
from datetime import date


def test_budget_event_without_stdev():
    amount = 100
    event = BudgetEvent(
        name='test_event',
        amount=amount,
        frequency_type='Monthly',
    )

    assert len(event.summary) == 12
    assert all(e.event_date.day == date.today().day for e in event.summary)
    assert all(e.min == -amount for e in event.summary)
    assert all(e.mean == -amount for e in event.summary)
    assert all(e.max == -amount for e in event.summary)


def test_budget_event_with_stdev():
    amount = 100
    stdev = 5
    event = BudgetEvent(
        name='test_event',
        amount=amount,
        frequency_type='Monthly',
        stdev=stdev,
    )

    assert len(event.summary) == 12
    assert all(e.event_date.day == date.today().day for e in event.summary)

    # TODO: very fuzzy tests...there has to be a better way
    assert len([e.min for e in event.summary if (-amount - e.min) < ((stdev * 3) + 2)]) >= 10
    assert len([e.min for e in event.summary if (-amount - e.min) > ((stdev * 2) - 2)]) >= 10
    assert len([e.mean for e in event.summary if (-amount + 2) > e.mean > (-amount - 2)]) >= 10
    assert len([e.max for e in event.summary if (e.max + amount) < ((stdev * 3) + 2)]) >= 10
    assert len([e.max for e in event.summary if (e.max + amount) > ((stdev * 2) - 2)]) >= 10
