import pytest

from dtb.currency import Currency


@pytest.fixture
def rub() -> Currency:
    return Currency(code="RUB", scale=1, sign="₽", default=True)
