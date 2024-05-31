from django.db import models
from django.utils import timezone

class Balance(models.Model):
    user = models.ForeignKey(to="account.User", on_delete=models.CASCADE, related_name='balance_user')
    balance = models.DecimalField(max_digits=13, decimal_places=2, default=0.00)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.save()
            Transaction.objects.create(balance=self, transaction_type='deposit', amount=amount)
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.save()
            Transaction.objects.create(balance=self, transaction_type='withdraw', amount=amount)
            return True
        return False


class Transaction(models.Model):
    TRANSACTION_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw')
    ]
    
    balance = models.ForeignKey(Balance, on_delete=models.CASCADE, related_name="transaction_user")
    transaction_type = models.CharField(max_length=8, choices=TRANSACTION_CHOICES)
    amount = models.DecimalField(max_digits=13, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.balance.user.username} - {self.get_transaction_type_display()} - {self.amount}"