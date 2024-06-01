from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models.functions import TruncDay
from django.db.models import Count, Sum, Case, When, F, DecimalField
from datetime import timedelta
from .models import Transaction, Balance
from .serializers import BalanceSerializer, TransactionSerializer, MyBalanceSerializer


class BalanceViewSet(ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MyBalanceSerializer
        return super().get_serializer_class()


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class MyBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        balance = Balance.objects.get(user=user)
        serializer = MyBalanceSerializer(instance=balance).data
        return Response(serializer)
    


class MyDailyTransactionsSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Текущая дата и время
        now = timezone.now()

        # Начало текущего месяца
        start_of_current_month = now.replace(day=1, hour=0)

        # Начало прошлого месяца
        start_of_last_month = (start_of_current_month - timedelta(days=1)).replace(day=1, hour=0)

        # Дата два месяца назад
        months_ago = now - timedelta(days=30)

        # Фильтрация транзакций за последний месяц
        transactions_last_months = Transaction.objects.filter(date__gte=months_ago, balance__user=user)

        # Агрегация данных с группировкой по пользователю и дням
        daily_user_summary = transactions_last_months.annotate(day=TruncDay('date')).values('balance__user', 'day').annotate(
            total_transactions=Count('id'),
            total_deposits=Sum(
                Case(
                    When(transaction_type='deposit', then=F('amount')),
                    default=0,
                    output_field=DecimalField()
                )
            ),
            total_withdraws=Sum(
                Case(
                    When(transaction_type='withdraw', then=F('amount')),
                    default=0,
                    output_field=DecimalField()
                )
            )
        ).order_by('balance__user', '-day')

        # Агрегация данных за текущий месяц
        current_month_summary = transactions_last_months.filter(date__gte=start_of_current_month,  balance__user=user).aggregate(
            total_transactions=Count('id'),
            total_deposits=Sum(
                Case(
                    When(transaction_type='deposit', then=F('amount')),
                    default=0,
                    output_field=DecimalField()
                )
            ),
            total_withdraws=Sum(
                Case(
                    When(transaction_type='withdraw', then=F('amount')),
                    default=0,
                    output_field=DecimalField()
                )
            )
        )

        # Агрегация данных за прошлый месяц
        last_month_summary = transactions_last_months.filter(date__gte=start_of_last_month, date__lt=start_of_current_month, balance__user=user).aggregate(
            total_transactions=Count('id'),
            total_deposits=Sum(
                Case(
                    When(transaction_type='deposit', then=F('amount')),
                    default=0,
                    output_field=DecimalField()
                )
            ),
            total_withdraws=Sum(
                Case(
                    When(transaction_type='withdraw', then=F('amount')),
                    default=0,
                    output_field=DecimalField()
                )
            )
        )

        response_data = {
            'daily_user_summary': daily_user_summary,
            'current_month_summary': current_month_summary,
            'last_month_summary': last_month_summary
        }

        return Response(response_data)
