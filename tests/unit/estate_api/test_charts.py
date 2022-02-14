from datetime import datetime
import pytest

from estate_api.charts import TimeSeriesChartData, HistogramChartData
from estate_api.models import Transaction


@pytest.mark.django_db
def test_time_series_chart_data_get_queryset_returns_dict_wthout_data(
    transaction_fixture: Transaction,
):
    """Assert that TimeSeriesChartData.get_queryset() method returns
    a dictionary with without data if there is only one instance of
    Transaction object in DB (with random fields).
    """
    postcode = "SW18"
    dates = [datetime(2005, 1, 1, 0, 0), datetime(2006, 3, 1, 1, 1)]
    chart_data = TimeSeriesChartData(postcode, *dates)
    assert chart_data.get_queryset() == {"SW18": {}}


@pytest.mark.django_db
def test_histogram_chart_data_get_queryset_returns_dict_wthout_data(
    transaction_fixture: Transaction,
):
    """Assert that HistogramChartData.get_queryset() method returns
    a dictionary with without data if there is only one instance of
    Transaction object in DB (with random fields).
    """
    postcode = "NE5"
    date = [datetime(2005, 1, 1, 0, 0)]
    chart_data = HistogramChartData(postcode, *date)
    assert chart_data.get_queryset() == {"NE5": {}}
