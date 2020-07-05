from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class shopEdit(ModelForm):
	class Meta:
		model = vendorShop
		fields = ['name','first_phone','second_phone','status']
		widgets = {
			'status': forms.Select(attrs={'class':'form-control'}),
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'first_phone': forms.NumberInput(attrs={'class': 'form-control'}),
			'second_phone': forms.NumberInput(attrs={'class': 'form-control'})
			}



class UserForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = '__all__'
		exclude = ['user']