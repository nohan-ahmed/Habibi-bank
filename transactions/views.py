from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, View
from transactions.models import Transaction
from datetime import datetime
from django.db.models import Sum
from . import forms
from .constants import TRANSACTION_TYPE
from accounts.models import UserBankAccount

# Create your views here.
class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = "./transactions/transaction_form.html"
    title = ""
    success_url = reverse_lazy('transaction_report')
    def get_form_kwargs(self):
        kwargs  = super().get_form_kwargs()
        kwargs.update({
            'account':self.request.user.account
        })
        return kwargs
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title'] = self.title
        return context
    
class DepositMoneyView(TransactionCreateMixin):
    form_class = forms.DepositForm
    title = 'Deposite money'
    def get_initial(self):
        initial = {'transaction_type':1}
        return initial
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields = ['balance']
        )
        messages.success(self.request,f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully')
        return super().form_valid(form)
    
class WithdrawalMoneyView(TransactionCreateMixin):
    form_class = forms.WithdrawForm
    title = 'Withdrawal Money'
    def get_initial(self):
        initial = {'transaction_type':2}
        return initial
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance -= amount
        
        account.save(
            update_fields = ['balance']
        )
        
        messages.success(self.request, f'Successfully withdrawn {"{:,.2f}".format(float(amount))}$ from your account')
        return super().form_valid(form)
    
class LoanRequestView(TransactionCreateMixin):
    form_class = forms.LoanRequestForm
    title = 'Request For Loan'
    def get_initial(self):
        initial = {'transaction_type':3}
        return initial
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        current_loan_count = Transaction.objects.filter(account=account, transaction_type=3, loan_aproved=True).count()
        if current_loan_count >= 3:
            return HttpResponse('You have crossed your limits')
        
        messages.success(self.request, f'Loan request for {"{:,.2f}".format(float(amount))}$ submitted successfully')
        return super().form_valid(form)


class TransactionReportView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = './transactions/transaction_report.html'
    balance = 0
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account = self.request.user.account
        )
        
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            queryset = queryset.filter(timestamp__date__gte = start_date, timestamp__date__lte = end_date)
            self.balance = Transaction.objects.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
            
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context.update({
            'account':self.request.user.account
        })
        return context
    

class PayLoanView(LoginRequiredMixin, View):
    def get(self, request,*args, **kwargs):
        loan = get_object_or_404(Transaction, id = kwargs.get('loan_id'))
        
        if loan.loan_aproved:
            user_account = loan.account
            if loan.amount < user_account.balance:
                user_account.balance -= loan.amount
                loan.balance_after_transaction = user_account.balance
                user_account.save()
                loan.transaction_type = 4
                loan.save()
                return redirect('loan_list')
            else:
                messages.error(request, message='Loan amount is greter then available balance.')
                return redirect('loan_list')
            

class LoanListView(LoginRequiredMixin, ListView):
    model= Transaction
    template_name = './transactions/loan_request.html'
    context_object_name = 'loans'
    
    def get_queryset(self):
        user_account = self.request.user.account
        QuerySet = Transaction.objects.filter(
            account=user_account,
            transaction_type=3
        )
        return QuerySet
    

class TransferMoneyView(View):
    template_name = "./transactions/transfer_money.html"
    
    def get(self, request, **kwargs):
        form = forms.TransferMoneyForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = forms.TransferMoneyForm(request.POST)
        if form.is_valid():
            print('inside')
            print(form.cleaned_data)  # Moved inside the is_valid() block
            amount = form.cleaned_data.get('amount')
            transfer_id = form.cleaned_data.get('transfer_id')
            current_account = request.user.account
            try:
                transfer_account = UserBankAccount.objects.get(account_no=transfer_id)
                current_account.balance -= amount
                transfer_account.balance += amount
                current_account.save()
                transfer_account.save()
                messages.success(request, f'Your transfer of ${amount} to {transfer_account} has been completed successfully.')
                
                Transaction.objects.create(
                    account = current_account,
                    amount = amount,
                    balance_after_transaction=current_account.balance,
                    transaction_type = 5,
                )
                
                Transaction.objects.create(
                    account = transfer_account,
                    amount = amount,
                    balance_after_transaction=transfer_account.balance,
                    transaction_type = 6,
                )
                
            except UserBankAccount.DoesNotExist:
                messages.error(request, f'Transfer account no {transfer_id} doesn\'t exist!')
        return redirect('transfer_money')  