from typing import Any
from django.contrib import admin
from .models import Transaction
# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id','account','amount','balance_after_transaction','transaction_type','timestamp','loan_aproved']

    def save_model(self, request, obj, form, change):
        if obj.loan_aproved:
            obj.account.balance += obj.amount
            obj.balance_after_transaction = obj.account.balance
            obj.account.save()
        return super().save_model(request, obj, form, change)