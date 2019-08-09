import pytest

from budgie.budget_event import BudgetEvent


@pytest.mark.parametrize('freq_type, summary_length', [
    ('OneTime', 1),
    ('Monthly', 12),
    ('BiWeekly', 27),
])
def test_budget_event_constant(freq_type, summary_length):
    amount = 100
    event = BudgetEvent(
        name='test_event',
        amount=amount,
        frequency_type=freq_type,
    )

    assert len(event.summary) == summary_length
    assert all(e.min == -amount for e in event.summary)
    assert all(e.mean == -amount for e in event.summary)
    assert all(e.max == -amount for e in event.summary)


@pytest.mark.parametrize('freq_type, summary_length', [
    ('OneTime', 1),
    ('Monthly', 12),
    ('BiWeekly', 27),
])
def test_budget_event_with_stdev(freq_type, summary_length):
    amount = 100
    stdev = 5
    event = BudgetEvent(
        name='test_event',
        amount=amount,
        frequency_type=freq_type,
        stdev=stdev,
    )

    assert len(event.summary) == summary_length

    # TODO: very fuzzy tests...there has to be a better way
    fuzzy = summary_length - 2
    assert len([e.min for e in event.summary if (-amount - e.min) < ((stdev * 3) + 2)]) >= fuzzy
    assert len([e.min for e in event.summary if (-amount - e.min) > ((stdev * 2) - 2)]) >= fuzzy
    assert len([e.mean for e in event.summary if (-amount + 2) > e.mean > (-amount - 2)]) >= fuzzy
    assert len([e.max for e in event.summary if (e.max + amount) < ((stdev * 3) + 2)]) >= fuzzy
    assert len([e.max for e in event.summary if (e.max + amount) > ((stdev * 2) - 2)]) >= fuzzy
