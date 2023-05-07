import pytest

from party_calc import calculator


@pytest.fixture()
def calc():
    return calculator.PartyCalculator()
