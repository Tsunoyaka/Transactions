from rest_framework import serializers
from .models import Transaction, Balance


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['id', 'balance', 'user']
        read_only_fields = ['balance']


class MyBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['id', 'balance', 'user']
        read_only_fields = ['balance']
           
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        all_transaction = TransactionSerializer(instance.transaction_user.order_by('-date'), many=True).data
        deposit = TransactionSerializer(instance.transaction_user.order_by('-date').filter(transaction_type='deposit'), many=True).data
        withdraw = TransactionSerializer(instance.transaction_user.order_by('-date').filter(transaction_type='withdraw'), many=True).data
        representation['all_transaction'] = all_transaction
        representation['deposit'] = deposit
        representation['withdraw'] = withdraw
        return representation

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'balance', 'transaction_type', 'amount', 'date']
        read_only_fields = ['date']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def create(self, validated_data):
        balance = validated_data['balance']
        amount = validated_data['amount']
        transaction_type = validated_data['transaction_type']

        if transaction_type == 'deposit':
            balance.deposit(amount)
        elif transaction_type == 'withdraw':
            if amount > balance.balance:
                raise serializers.ValidationError("Insufficient balance.")
            balance.withdraw(amount)
        else:
            raise serializers.ValidationError("Invalid transaction type.")
        return super().create(validated_data)
