from django.db import models

from config.mixins import TimeStampedModel, UUIDPrimaryKeyAbstractModel


class Transaction(UUIDPrimaryKeyAbstractModel, TimeStampedModel):
    """Model storing information on property sales in England and Wales."""

    DETACHED = "D"
    SEMI_DETACHED = "S"
    TERRACED = "T"
    FLAT_MAISONETTE = "F"
    OTHER = "O"
    PROPERTY_TYPE_CHOICES = [
        (DETACHED, "detached"),
        (SEMI_DETACHED, "semi-detached"),
        (TERRACED, "terraced"),
        (FLAT_MAISONETTE, "flat-maisonette"),
        (OTHER, "other"),
    ]
    price_paid = models.IntegerField(help_text="Price paid [£]")
    transaction_date = models.DateField(help_text="Date of transaction")
    postcode = models.CharField(max_length=8, help_text="Postal code")
    property_type = models.CharField(
        max_length=1,
        choices=PROPERTY_TYPE_CHOICES,
        help_text="Type of property",
    )
