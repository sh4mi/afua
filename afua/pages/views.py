from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm,informationUser,vendorUser
# from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from.models import Information
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

def vendor(request):
    form = vendorUser()
    if request.method == 'POST':
        form = vendorUser(request.POST)
    if form.is_valid():
        form.save()
        return redirect('login')
    else:
       context = {'form': form}
       return render(request, 'pages/vendor.html', context)


def information(request):
    form = informationUser()
    if request.method == 'POST':
        form = informationUser(request.POST)
    if form.is_valid():
        form.save()
        return redirect('login')
    else:
       context = {'form': form}
       return render(request, 'pages/information.html', context)



def loginPage(request):

     if request.method=='POST':
        username=request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            context = {}
            messages.info(request,'Username or Password is incorrect')
            return render(request, 'pages/login.html', context)
     else:
      context = {}
     return render(request, 'pages/login.html', context)

def logoutUser(request):
        logout(request)
        return redirect('login')
# @login_required(login_url='login')


def registerPage(request):

     form=CreateUserForm()
     if request.method=='POST':
      form = CreateUserForm(request.POST)
     if form.is_valid():
         form.save()
         user=form.cleaned_data.get('username')
         messages.success(request,'Account was created for ' + user)
         return redirect('information')
     else:
         context = {'form': form}
         return render(request, 'pages/register.html', context)