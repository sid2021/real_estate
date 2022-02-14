from datetime import datetime
from typing import Optional
import pytest

from estate_api.utils import parse_date, validate_postalcode


@pytest.mark.parametrize(
    "date,expected_value, raises_exception",
    [
        ("2020-01", datetime(2020, 1, 1, 0, 0), False),
        ("2020-01-01", None, True),
        (2020, None, True),
    ],
)
def test_parse_date(
    date: str, expected_value: datetime, raises_exception: bool
) -> None:
    """Assert that parse_date() function returns correct value."""
    if raises_exception:
        with pytest.raises((ValueError, TypeError)):
            parse_date(date)
    else:
        assert parse_date(date) == expected_value


@pytest.mark.parametrize(
    "postcode,expected_value",
    [
        ("SW18", "SW18"),
        ("E17", "E17"),
        ("L1", "L1"),
        ("", None),
        (None, None),
        ("BH1 1QY", None),
    ],
)
def test_validate_postalcode(
    postcode: str,
    expected_value: Optional[str],
) -> None:
    """Assert that validate_postalcode() function returns correct value."""
    assert validate_postalcode(postcode) == expected_value
