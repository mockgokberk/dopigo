from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api
from .api import (AccountsViewSet, BalanceHistoryViewSet, CustomerViewSet)

router = DefaultRouter(trailing_slash=False)
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'accounts', AccountsViewSet, basename='account')
router.register(r'history_balance', BalanceHistoryViewSet, basename='history_balance')
urlpatterns = router.urls

urlpatterns += (
    path('transfer_balance', api.TransferBalance.as_view()),
)
