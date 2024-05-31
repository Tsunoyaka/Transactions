# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, TransactionView, BuyView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('transaction/', TransactionView.as_view(), name='transaction'),
    path('buy/', BuyView.as_view(), name='buy'),
]
