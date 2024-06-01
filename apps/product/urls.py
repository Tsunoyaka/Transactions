from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionView, BuyView

urlpatterns = [
    path('transaction/', TransactionView.as_view(), name='transaction'),
    path('buy/', BuyView.as_view(), name='buy'),
]
