from django.urls import include, path
from rest_framework import routers

from estate_api.views import TransactionViewSet

router = routers.DefaultRouter()
router.register(r"transactions", TransactionViewSet, basename="transaction")

urlpatterns = [path("", include(router.urls))]
