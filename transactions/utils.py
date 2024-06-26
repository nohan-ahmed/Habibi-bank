from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


def TransactionMail(sub, to_user, amount, transfer_account=None, transaction_id=None):
    text = f"Your {sub} request for ${amount} has been successfully completed.".capitalize()
    if sub == 'Loan request':
        text = f'Your ${amount} loan request is currently pending. After bank approval you will get a confirmation mail and the loan amount will be added to your account.'
    elif sub.lower() == 'transfer money':
        sub=f' ${amount} successfully transferred'
        text = f'Your transfer of ${amount} to {transfer_account} has been processed successfully.Transaction ID: {transaction_id}. For further details, please check your transaction history.'
    
    elif sub.lower() == 'receive money':
        sub=f' ${amount} Payment Received'
        text = f'You have received ${amount} from {transfer_account}. Transaction ID: {transaction_id}. For any queries, please contact our support team.'
        
    elif sub.lower() == 'loan approval':
        sub = "Congratulations, Your Loan is Approved!"
        text = f'Congratulations! Your loan application for ${amount} has been approved. The funds will be disbursed to your account shortly. Thank you for choosing us for your financial needs.'
    else:
        sub+=' Successful'.capitalize()

    message = render_to_string('./transactions/transaction_mail.html', {
        'user': to_user,
        'message':text,
    })
    
    to_mail = to_user.email
    send_mail = EmailMultiAlternatives(sub, '', to=[to_mail])
    send_mail.attach_alternative(message, 'text/html')
    send_mail.send()
