from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class User(AbstractUser):
    USER_CHOICES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('contractor', 'Contractor'),
    )
    user_type = models.CharField(max_length=20,default='customer', choices=USER_CHOICES)
    activation_key = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return '%s ' % (self.username)


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile' )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default='', blank=True)
    bio = models.TextField(default='', blank=True)
    first_phone = models.CharField(max_length=20, blank=True, default='')
    second_phone = models.CharField(max_length=20, blank=True, default='')
    city = models.CharField(max_length=100, default='', blank=True)
    Nic = models.CharField(max_length=50, blank=True, default='')
    country = models.CharField(max_length=100, default='', blank=True)
    address = models.CharField(max_length=100, default='', blank=True)
    shopname = models.CharField(max_length=100, default='', blank=True)
    picture = models.ImageField(default="profile1.png",blank=True)
    


def __str__(self):
        return 'Profile of user: {}'.format(self.user.username)

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)

class vendorShop(models.Model):
    Owner = models.OneToOneField(User, on_delete=models.CASCADE)
    select = (
        ('on','ON'),
        ('off','OFF'),
    )
    status = models.CharField(max_length=10, choices=select, default='', blank=True)
    name = models.CharField(max_length=20, blank=True, default='')
    first_phone = models.CharField(max_length=20, blank=True, default='')
    second_phone = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        return self.name