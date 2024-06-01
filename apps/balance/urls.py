from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BalanceViewSet, TransactionViewSet, MyBalanceView, MyDailyTransactionsSummaryView

router = DefaultRouter()
router.register(r'balances', BalanceViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('my-balance/', MyBalanceView.as_view()),
    path('my-tran/', MyDailyTransactionsSummaryView.as_view()),
]
