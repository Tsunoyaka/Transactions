from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import Product, ProductInfo
from .serializers import ProductSerializer
from apps.balance.models import Balance
from rest_framework import status

User = get_user_model()

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    

class TransactionView(APIView):
    def post(self, request):
        seller_key = request.data.get('key')
        cost = request.data.get('cost')
        buyer_email = request.data.get('email')
        if User.objects.filter(email=buyer_email).exists():
            seller = User.objects.filter(key=seller_key).first()
            buyer = User.objects.filter(email=buyer_email).first()
            code = self.send_pay_code(email=buyer_email)
            ProductInfo.objects.create(seller=seller, buyer=buyer, cost=cost, code=code)
            return Response('Введите код для покупки')
        return Response('Пользователь с такой почтой не найден!', status=status.HTTP_404_NOT_FOUND)
        
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
        
        
class BuyView(APIView):
    def post(self, request):
        code = request.data.get('code')
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
            return Response('У вас недостаточно средств', status=status.HTTP_204_NO_CONTENT)
        seller_balance.deposit(amount=cost)
        buyer_balance.withdraw(amount=cost)
        return Response('Вы успешно купили товар', status=status.HTTP_200_OK)
        # seller_key = request.data.get('key')
        # email = request.data.get('email')
        # code = request.data.get('code')
        # cost = request.data.get('cost')
        # seller = User.objects.filter(id=seller_key).first()
        # buyer = User.objects.filter(email=email, activation_code=code).first()
        # seller_balance = Balance.objects.filter(user=seller).first()
        # buyer_balance = Balance.objects.filter(user=buyer).first()
        # if cost > buyer_balance.balance:
        #     return Response('У вас недостаточно средств')
        # seller_balance.deposit(amount=cost)
        # buyer_balance.withdraw(amount=cost)
        # return Response('Вы успешно купили товар')