from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


# class informationUser(ModelForm):
#     class Meta:
#         model= Information
#         fields='__all__'

# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model=User
#         fields=['username','email','password1','password2']

# class vendorUser(ModelForm):
#     class Meta:
#         model= Vendor
#         fields= '__all__'