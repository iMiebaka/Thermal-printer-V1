from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class Drug(models.Model):
    name = models.CharField(max_length=20, null=True, unique=True)
    drug_test = models.CharField(max_length=10)
    desc = models.CharField(max_length=30, default='')
    code_name = models.CharField(max_length=10, null=True)
    amount = models.PositiveIntegerField()
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete = models.SET_NULL)
    created_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return '%s | %s' %(self.code_name, self.name)


class Treatment(models.Model):
    name = models.CharField(max_length=20, unique=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    created_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class Prescription(models.Model):
    treating = models.ForeignKey('Treatment', related_name='treatment_given', on_delete=models.CASCADE)
    drug = models.ForeignKey('Drug', related_name='drugs_prescribed', null=True, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    created_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.treating.name

class History(models.Model):
    qty = models.CharField(max_length=2)
    product = models.CharField(max_length=20)
    mode_of_payment = models.CharField(max_length=5)
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='payment_by', null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField()
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='clearance_office', on_delete = models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return self.product

    @property
    def hihi(self):
        return 'Hello World'
    
