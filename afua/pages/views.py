from django.shortcuts import render,redirect
# from django.contrib.auth.forms import UserCreationForm
# from .forms import CreateUserForm,informationUser,vendorUser
# from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# from.models import Information
from .import forms

def home(requset):
    return render(requset, 'pages/landing.html')

def about(requset):
    return render(requset, 'pages/about-us.html')

def contact(requset):
    return render(requset, 'pages/contact.html')

def services(requset):
    return render(requset, 'pages/services.html')

def typepaint(requset):
    return render(requset, 'pages/typepaint.html')

def typecement(requset):
    return render(requset, 'pages/typecement.html')



def logoutUser(request):
        logout(request)
        return redirect('login')
# @login_required(login_url='login')


# def registerPage(request):

#      form=CreateUserForm()
#      if request.method=='POST':
#       form = CreateUserForm(request.POST)
#      if form.is_valid():
#          form.save()
#          user=form.cleaned_data.get('username')
#          messages.success(request,'Account was created for ' + user)
#          return redirect('information')
#      else:
#          context = {'form': form}
#          return render(request, 'pages/register.html', context)