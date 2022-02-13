from datetime import datetime
from typing import List, Optional, Tuple

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from estate_api.charts import HistogramChartData, TimeSeriesChartData
from estate_api.exceptions import InvalidTransactionParams
from estate_api.taxonomies import NUMBER_ENDPOINT_SCHEMA, PRICES_ENDPOINT_SCHEMA
from estate_api.utils import parse_date, validate_postalcode


class TransactionViewSet(viewsets.GenericViewSet):
    """Transaction viewset class."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _clean_params(
        self, postcode: str, dates: List
    ) -> Optional[Tuple[str, datetime, datetime]]:
        """Validate and return cleaned parameters.
        Date has to be in yyyy-mm format.
        Location has to be a valid postal code (outward code only) consisting
        of letters and digits only matching England or Wales format.
        """
        postcode = validate_postalcode(postcode)
        if not postcode:
            raise InvalidTransactionParams(
                "Please specify outward postal code (area and district)."
            )

        parsed_dates = []
        for date in dates:
            try:
                parsed_dates.append(parse_date(date))
            except (ValueError, TypeError):
                raise InvalidTransactionParams(
                    "Please specify date in yyyy-mm format."
                )

        return postcode, parsed_dates

    @swagger_auto_schema(responses={status.HTTP_200_OK: PRICES_ENDPOINT_SCHEMA})
    @action(detail=False, methods=["get"])
    def prices(self, request: Request) -> Response:
        """Return data to generate a time series chart of avarage prices for the
        given postcode and between the given from and to dates.
        """
        postcode = request.data.get("location")
        from_date = request.data.get("from")
        to_date = request.data.get("to")
        postcode, dates = self._clean_params(postcode, [from_date, to_date])
        transactions = TimeSeriesChartData(postcode, *dates).get_queryset()

        return Response(transactions, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: NUMBER_ENDPOINT_SCHEMA})
    @action(detail=False, methods=["get"])
    def numbers(self, request: Request) -> Response:
        """Return data to generate a histogram showing the number of transactions
        at various price brackets.
        """
        postcode = request.data.get("location")
        date = request.data.get("date")
        postcode, date = self._clean_params(postcode, [date])
        transactions = HistogramChartData(postcode, *date).get_queryset()

        return Response(transactions, status=status.HTTP_200_OK)
