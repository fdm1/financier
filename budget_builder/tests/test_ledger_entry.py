# pylint: disable=missing-docstring
import pytest
from budget_builder.ledger_entry import _to_currency


@pytest.mark.parametrize('input_val,output_val',
                         [[1, "$1.00"],
                          [2.5, "$2.50"],
                          [2.5212, "$2.52"],
                          [-2.5, "$2.50"],
                          ["5", "5"],
                          ["", ""],
                          ["foobar", "foobar"]])
def test_to_currency(input_val, output_val):
    assert _to_currency(input_val) == output_val
