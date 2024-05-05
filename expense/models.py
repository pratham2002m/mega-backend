from django.db import models
from django.utils import timezone
from django import forms
from datetime import datetime
import uuid

class UserModel(models.Model):
    username = models.CharField(max_length=100, unique=True, null=False, blank=False )
    email = models.CharField(max_length=100,null=False, blank=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    last_login = models.DateTimeField(default=datetime.now)
    password = models.CharField(max_length=20, null=False, blank=False)
    currmonth = models.IntegerField(default=1)
    currexpense = models.IntegerField(default=0)
    budget = models.IntegerField(default=10000)
    debts = models.JSONField(verbose_name="Debts", default={})

    def __str__(self):
        return self.username


class Expense(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    # id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False, blank=False )
    date = models.DateTimeField(default=datetime.now)
    text = models.CharField(max_length=2000)
    transtype = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    payment_mode = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
