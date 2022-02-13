"""Estate_api taxonomies module."""

from estate_api.models import Transaction

BRACKETS_NUM = 8
INPUT_DATE_FORMAT = "%Y-%m"
SERIES_CHART_DATE_FORMAT = "%Y-%m-%d"
INVALID_PARAMS_MSG = "Parameters validation error."

PROPERTY_TYPES = [
    Transaction.DETACHED,
    Transaction.SEMI_DETACHED,
    Transaction.TERRACED,
    Transaction.FLAT_MAISONETTE,
]

PRICES_ENDPOINT_SCHEMA = """
Example response schema:
{
    "SW18": {
        "D": {"2015-01-12": 600000, "2015-01-19": 1000000},
        "F": {"2015-01-09": 1160000, "2015-01-16": 1887500},
}
}"""

NUMBER_ENDPOINT_SCHEMA = """
Example response schema:
{
    "SW18": {
        "(1030000.0, 1220000.0]": 4,
        "(1410000.0, 1600000.0]": 8,
        "(270000.0, 460000.0]": 2,
    }
}
"""
