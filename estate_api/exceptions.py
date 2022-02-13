"""Estate_api exceptions module."""

from rest_framework import serializers

from estate_api.taxonomies import INVALID_PARAMS_MSG


class InvalidTransactionParams(serializers.ValidationError):
    """Exception raised when request parameters are invalid."""

    def __init__(self, message, *args, **kwargs):
        detail = f"{INVALID_PARAMS_MSG} {message}"
        super().__init__(detail, *args, **kwargs)
