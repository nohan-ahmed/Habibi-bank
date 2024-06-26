# Generated by Django 5.0.3 on 2024-06-24 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_rename_load_aproved_transaction_loan_aproved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.IntegerField(choices=[(1, 'Deposite'), (2, 'Withdrawal'), (3, 'Loan'), (4, 'Loan paid'), (5, 'Send money'), (6, 'Received money')], null=True),
        ),
    ]
