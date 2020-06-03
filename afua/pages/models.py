from django.db import models

class Information(models.Model):
    Type = (
        ('Vendor', 'Vendor'),
        ('Contractor', 'Contractor'),
        ('User', 'User'),
    )
    fname = models.CharField(max_length=200, null=True)
    lname = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    account = models.CharField(max_length=200, null=True, choices=Type)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.fname

class Vendor(models.Model):
    name = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    code = models.IntegerField(max_length=200, null=True)
    fname = models.CharField(max_length=200, null=True)
    lname = models.CharField(max_length=200, null=True)
    contact = models.IntegerField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name



