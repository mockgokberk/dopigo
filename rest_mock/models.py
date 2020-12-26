from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=30)


class Account(models.Model):
    deposit = models.FloatField(default=0)
    customer = models.ForeignKey(Customer, on_delete= models.DO_NOTHING)

class BalanceHistory(models.Model):
    timeslot = models.DateTimeField()
    account = models.ForeignKey(Account,on_delete= models.DO_NOTHING )
    value = models.FloatField()
