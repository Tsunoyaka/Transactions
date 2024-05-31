from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BalanceViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'balances', BalanceViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
