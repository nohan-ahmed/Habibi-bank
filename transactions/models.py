from django.db import models
from accounts.models import UserBankAccount
from .constants import TRANSACTION_TYPE
# Create your models here.
class Transaction(models.Model):
    account = models.ForeignKey(to=UserBankAccount, related_name = 'transaction', on_delete= models.CASCADE)
    amount = models.DecimalField(max_digits = 12, decimal_places  = 2)
    balance_after_transaction=models.DecimalField(max_digits = 12, decimal_places  = 2)
    transaction_type = models.IntegerField(choices = TRANSACTION_TYPE , null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    loan_aproved = models.BooleanField(default=False)
    class Meta:
        ordering = ['timestamp']