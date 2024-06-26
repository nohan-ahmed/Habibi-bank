from django.db import models

# Create your models here.
class BankModel(models.Model):
    is_bankrupt = models.BooleanField(default=True)
    