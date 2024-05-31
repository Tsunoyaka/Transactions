from django.db import models
from django.utils import timezone

class Product(models.Model):
    user = models.ForeignKey(to="account.User", on_delete=models.CASCADE, related_name='user_product')
    cost = models.DecimalField(verbose_name='Стоимость', max_digits=13, decimal_places=3)


class ProductInfo(models.Model):
    seller = models.ForeignKey(to="account.User", on_delete=models.CASCADE, related_name='seller_info')
    buyer_email = models.ForeignKey(to="account.User", on_delete=models.CASCADE, related_name='buyer_info')
    cost = models.DecimalField(verbose_name='Стоимость', max_digits=13, decimal_places=3)
    date = models.DateTimeField(verbose_name='Дата',default=timezone.now)
    code = models.CharField(max_length=8)
    
