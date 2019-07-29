from freezegun import freeze_time
import pytest


@pytest.fixture(autouse=True)
def set_date():
    with freeze_time("2019-01-01"):
        yield
