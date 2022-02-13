import re
from datetime import datetime
from typing import Optional

from estate_api.taxonomies import INPUT_DATE_FORMAT

# These are a match: 'E4', 'E17', 'BN43'
OUTWARD_CODE_REGEX = re.compile(r"^[0-9A-Z]{2,4}$")


def parse_date(date: str) -> Optional[datetime]:
    """Parse date and return the datetime object or raise exception."""
    try:
        return datetime.strptime(date, INPUT_DATE_FORMAT)
    except (ValueError, TypeError) as e:
        raise e


def validate_postalcode(postcode: str) -> Optional[re.Match]:
    """Validate postal code. We are expecting to receive from frontend
    only the outward code (area and district) e.g. 'SW18' which is between
    two and four characters long.
    """
    if match := re.match(OUTWARD_CODE_REGEX, postcode):
        return match.group()
