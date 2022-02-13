from django.contrib import admin

from estate_api.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_date",
        "price_paid",
        "postcode",
        "property_type",
    )
