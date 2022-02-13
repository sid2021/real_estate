"""Load data from .csv file."""

import csv
from collections import namedtuple
from datetime import datetime

from django.conf import settings
from django.core.management import BaseCommand

from estate_api.models import Transaction
from estate_api.taxonomies import SERIES_CHART_DATE_FORMAT

HEADINGS = [
    "transaction_id",
    "price_paid",
    "transaction_date",
    "postcode",
    "property_type",
    "new_build",
    "estate_type",
    "paon",
    "saon",
    "street",
    "town",
    "district",
    "locality",
    "county",
    "record_status",
    "transaction_category",
]


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        """Command main entry-point"""
        self.load_data()

    def load_data(self):
        """Load data from "pp-complete.csv" file stored in project's root
        folder. Due to necessity to parse a huge CSV (~4.6 GB) import process
        might take up to ~10 hours.
        """
        with open(f"{settings.BASE_DIR}/pp-complete.csv") as f:
            f_csv = csv.reader(f)
            Row = namedtuple("Row", HEADINGS)
            for r in f_csv:
                row = Row(*r)
                Transaction.objects.create(
                    price_paid=int(row.price_paid),
                    transaction_date=datetime.strptime(
                        row.transaction_date.split(" ")[0],
                        SERIES_CHART_DATE_FORMAT,
                    ),
                    postcode=row.postcode,
                    property_type=row.property_type,
                )
