from datetime import datetime

import factory
from faker import Faker

from estate_api.models import Transaction

fake = Faker()

DATE_START = datetime(1997, 1, 1)
DATE_END = datetime(2020, 1, 30)


class TransactionFactory(factory.django.DjangoModelFactory):
    """Create Transaction model for tests."""

    price_paid = fake.random.randint(1, 5000000)
    transaction_date = fake.date_between_dates(
        date_start=DATE_START, date_end=DATE_END
    )
    postcode = fake.random_element(elements=("SW18 5TN", "NE5 1NY", "DL10 7NJ"))

    class Meta:
        model = Transaction
