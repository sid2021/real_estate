import calendar
from datetime import datetime
from typing import Dict

import pandas as pd
from django.db.models import Q

from estate_api.models import Transaction
from estate_api.taxonomies import (
    BRACKETS_NUM,
    PROPERTY_TYPES,
    SERIES_CHART_DATE_FORMAT,
)


class BaseChartData:
    """Base class in the chart data hierarchy. Can be used in the future to
    implement additional functionality shared with its children.
    """

    def __init__(self, postcode: str) -> None:
        self.postcode = postcode


class TimeSeriesChartData(BaseChartData):
    def __init__(self, postcode: str, *dates: datetime) -> None:
        super().__init__(postcode)
        self.from_date = dates[0].date()
        self.to_date = (
            dates[1]
            .replace(day=calendar.monthrange(dates[1].year, dates[1].month)[1])
            .date()
        )

    def get_queryset(self) -> Dict:
        """Return average house prices over time data to generate charts
        by frontend.

        Returned data schema:
        {
            "SW18": {
                "D": {
                    "2015-01-12": 600000,
                    "2015-01-19": 1000000,
                    (...)
                },
                "F": {
                    "2015-01-09": 1160000,
                    "2015-01-16": 1887500,
                    (...)
                },
                (...)
            }
        }

        Returned data is based on all transactions for the given postcode and
        between the given from and to dates.
        """
        # In DB we store full postal code e.g. "L15 8AL". We use iregex to query
        # for transactions which postalcode's outwatd code is an exact match i.e.
        # we should not get a match if we are looking for "L1" code.
        queryset = Transaction.objects.filter(
            Q(transaction_date__gte=self.from_date)
            & Q(transaction_date__lte=self.to_date),
            postcode__iregex=r"^(" + self.postcode + ") [0-9A-Z]{3}$",
        )

        data = {}
        for type in PROPERTY_TYPES:
            dataset = [d for d in queryset if d.property_type == type]
            if dataset:
                data[type] = dataset

        cleaned_data = {}
        cleaned_data[self.postcode] = {k: dict() for k in data.keys()}
        for type, dataset in data.items():
            dates = sorted(list(set(d.transaction_date for d in dataset)))
            for date in dates:
                transactions_for_date = [
                    d.price_paid for d in dataset if d.transaction_date == date
                ]
                avg_for_date = sum(transactions_for_date) / len(
                    transactions_for_date
                )
                cleaned_data[self.postcode][type][
                    date.strftime(SERIES_CHART_DATE_FORMAT)
                ] = int(avg_for_date)

        return cleaned_data


class HistogramChartData(BaseChartData):
    def __init__(self, postcode: str, date: datetime) -> None:
        super().__init__(postcode)
        self.from_date = date.date()
        self.to_date = date.replace(
            day=calendar.monthrange(date.year, date.month)[1]
        ).date()

    def get_queryset(self) -> Dict:
        """Return data to generate charts by frontend.

        Returned data schema:
        {
            "SW18": {
                "(1030000.0, 1220000.0]": 4,
                "(1410000.0, 1600000.0]": 8,
                "(270000.0, 460000.0]": 2,
                (...)
            }
        }

        Returned data is based on all transactions for the given postcode and
        month grouped in price brackets.
        """
        queryset = Transaction.objects.filter(
            Q(transaction_date__gte=self.from_date)
            & Q(transaction_date__lte=self.to_date),
            postcode__iregex=r"^(" + self.postcode + ") [0-9A-Z]{3}$",
        )

        df = pd.DataFrame(queryset.values_list("price_paid"), columns=["price"])
        try:
            df["bin"] = pd.cut(df["price"], bins=BRACKETS_NUM).astype(str)
            df2 = df.groupby("bin").bin.count()
        except ValueError:
            return {self.postcode: {}}

        return {self.postcode: df2.to_dict()}
