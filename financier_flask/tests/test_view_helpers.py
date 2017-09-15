# pylint: disable=missing-docstring

import pytest
from financier_flask.utils.view_helpers import extract_float, float_to_currency


@pytest.mark.parametrize('input_val,output_val',
                         [["1", 1.0],
                          ["2.5", 2.5],
                          ["-2.5", -2.5],
                          ["", 0.0],
                          ["foobar", 0.0]])
def test_extract_float(input_val, output_val):
    assert extract_float(input_val) == output_val


@pytest.mark.parametrize('input_val,output_val',
                         [["1", "$1.00"],
                          ["2.5", "$2.50"],
                          ["2.5212", "$2.52"],
                          ["-2.5", "$-2.50"],
                          ["", "$0.00"],
                          ["foobar", "$0.00"]])
def test_float_to_currency(input_val, output_val):
    assert float_to_currency(input_val) == output_val
