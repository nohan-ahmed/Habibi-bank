from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type']
    
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account') # account value ke pop kore anlam
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True # ei field disable thakbe
        self.fields['transaction_type'].widget = forms.HiddenInput() # user er theke hide kora thakbe
    
    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()

    
class DepositForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        min_deposit_amount = 100
        if amount < min_deposit_amount:
            raise forms.ValidationError( f'You need to deposit at least ${min_deposit_amount}')
        return amount
    


class WithdrawForm(TransactionForm):
    def clean_amount(self):
        account = self.account
        amount = self.cleaned_data.get('amount')
        balance = account.balance
        min_withdraw_amount = 100
        max_withdraw_amount = 200000
        
        if amount < min_withdraw_amount:
            raise forms.ValidationError( f'You can withdraw at least ${min_withdraw_amount}')
        elif amount> max_withdraw_amount:
            raise forms.ValidationError( f'You can withdraw at most ${min_withdraw_amount}')
        elif amount > balance:
            raise forms.ValidationError(f'You don\'t have enough balance. Your current balance ${balance}')
        return amount

class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        return amount


class TransferMoneyForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    transfer_id = forms.IntegerField()
