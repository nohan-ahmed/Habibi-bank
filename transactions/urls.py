from django.urls import path
from transactions.views import TransferMoneyView,DepositMoneyView, WithdrawalMoneyView, LoanRequestView, PayLoanView, LoanListView, TransactionReportView

urlpatterns = [
    path('deposit/', DepositMoneyView.as_view(), name='deposit_money'),
    path('withdraw/', WithdrawalMoneyView.as_view(), name='withdraw_money'),
    path('loan-request/', LoanRequestView.as_view(), name='loan_request'),
    path('pay-loan/<int:loan_id>', PayLoanView.as_view(), name='pay_loan'),
    path('loan-list/', LoanListView.as_view(), name='loan_list'),
    path('transaction-report/', TransactionReportView.as_view(), name='transaction_report'),
    path('transfer-money/', TransferMoneyView.as_view(), name='transfer_money'),
]
