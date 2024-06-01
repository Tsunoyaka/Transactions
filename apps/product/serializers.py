from rest_framework import serializers

class ProductInfoSerializer(serializers.Serializer):
    seller_key = serializers.CharField(max_length=24, required=True) # Уникальный ключ "продавца", который он получает в личном кабинете
    cost = serializers.DecimalField(max_digits=13, decimal_places=3, required=True)
    buyer_email = serializers.EmailField(required=True) # Почта пользователя, которая вводится со стороны "продавца"
    