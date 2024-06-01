from django.db import models

class ProductInfo(models.Model):
    seller = models.ForeignKey(to="account.User", on_delete=models.CASCADE, related_name='seller_info')
    buyer_email = models.ForeignKey(to="account.User", on_delete=models.CASCADE, related_name='buyer_info')
    cost = models.DecimalField(verbose_name='Стоимость', max_digits=13, decimal_places=3)
    date = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
    code = models.CharField(max_length=8)
    
    def save(self, *args, **kwargs):
        if ProductInfo.objects.exists():
            ProductInfo.objects.all().delete()
        super(ProductInfo, self).save(*args, **kwargs)