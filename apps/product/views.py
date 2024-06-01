from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from drf_yasg.utils import swagger_auto_schema
from apps.balance.models import Balance
from .models import ProductInfo
from .serializers import ProductInfoSerializer

User = get_user_model()

class TransactionView(APIView):
    @swagger_auto_schema(request_body=ProductInfoSerializer)
    def post(self, request):
        serializer = ProductInfoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            seller_key = serializer.data.get('seller_key')
            cost = serializer.data.get('cost')
            buyer_email = serializer.data.get('buyer_email')
            if User.objects.filter(email=buyer_email).exists():
                seller = User.objects.filter(key=seller_key).first()
                buyer = User.objects.filter(email=buyer_email).first()
                code = self.send_pay_code(email=buyer_email) # Отправка кода для интернет покупки пользователю
                ProductInfo.objects.create(seller=seller, buyer_email=buyer, cost=cost, code=code)
                return self.html_response(cost=cost) # Отправка формы оплаты "продавцу"
        return self.html_false()
    
        
    def send_pay_code(self, email):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            subject='Pay Code',
            message=f'Ваш код для интернет покупки {user.activation_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )
        return user.activation_code
    
    def html_response(self, cost):
        html_message = render_to_string(
        'product/index.html', 
        {'price': cost}
        )
        return HttpResponse(html_message, content_type="text/html", status=status.HTTP_200_OK)
    
    def html_false(self):
        html_message = render_to_string(
        'product/false.html'
        )
        return HttpResponse(html_message, content_type="text/html", status=status.HTTP_404_NOT_FOUND)    
        
class BuyView(APIView):
    def post(self, request):
        code = request.data.get('code') # Код пользователя, которую он получает с почты
        product_filter = ProductInfo.objects.filter(code=code)
        if not product_filter.exists():
            return Response('Неверный код', status=status.HTTP_400_BAD_REQUEST)
        product = product_filter.first()
        seller = product.seller
        buyer = product.buyer_email
        cost = product.cost
        seller_balance = Balance.objects.get(user=seller)
        buyer_balance = Balance.objects.get(user=buyer)
        if cost > buyer_balance.balance:
            return Response('У вас недостаточно средств', status=status.HTTP_400_BAD_REQUEST)
        seller_balance.deposit(amount=cost)
        buyer_balance.withdraw(amount=cost)
        product.delete() # Удаляем информацию о приобритаемом "продукте" для претодвращения повторной покупки по одному и тому же коду
        return Response('Вы успешно купили товар', status=status.HTTP_200_OK)