from django.views import generic
from django.urls import reverse_lazy

from django.contrib.auth import login, authenticate,logout
from django.shortcuts import render, redirect
from .forms import *
import uuid
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .decorators import unauthenticated_user,allowed_users,admin_only
User = get_user_model()

unauthenticated_user
def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user != None:
            login(request, user)
            if user.user_type == "customer":
                return redirect('home')
            elif user.user_type == "vendor":
                return redirect('accountview')
            else:
                return render(request,'pages/accountsetting')
        else:
            context = {}
            messages.info(request,'Username or Password is incorrect')
            return render(request, 'pages/login2.html', context)
    else:
        context = {}
        return render(request, 'pages/login2.html', context)

def logoutUser(request):
        logout(request)
        return redirect('login')

# Create your views here.
unauthenticated_user
def registerPage(request):
    errors = []
    if request.method == 'POST':
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        # country = request.POST.get("country", "")
        if email and username and password :
            try:
                user,created = User.objects.get_or_create(username=username, email=email)
                if created:
                    # user.user_type=3
                    user.user_type = 'customer'
                    user.set_password(password)
                    user.activation_key = uuid.uuid4().hex[:30]
                    
                    if settings.ENABLE_USER_ACTIVATION:
                        user.is_active = False
                        user.save()
                        msg = "http://127.0.0.1:8000/activate/"+user.activation_key
                        subject = 'Thank you for registering to our site'
                        message = ' Please click this link to verify your account '+msg
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [user.email]
                        send_mail(subject, message, email_from, recipient_list)
                        return redirect('verify')
                    else:
                        user.is_active = True
                        user.save()
                        return redirect('login')
                else:
                    # user was retrieved
                    errors.append("user already exist. please use some other email")
            except IntegrityError as e:
                errors.append("user already exist. please use some other email")
            
            
        else:
            # request was empty
            errors.append("Please fill the form.")
            
    return render(request, 'pages/register.html',{'errors':errors})

unauthenticated_user
def registerVendorPage(request):
    errors = []
    if request.method == 'POST':
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        first_phone = request.POST.get("first_phone", "")
        second_phone = request.POST.get("second_phone", "")
        cnic = request.POST.get("cnic", "")
        country = request.POST.get("country", "")
        city = request.POST.get("city", "")
        gender = request.POST.get("gender", "")
        if email and username and password :
            try:
                user,created = User.objects.get_or_create(username=username, email=email)
                if created:
                    # user.user_type=3
                    user.user_type = 'vendor'
                    user.set_password(password)
                    user.activation_key = uuid.uuid4().hex[:30]
                    user.profile.first_phone = first_phone
                    user.profile.second_phone = second_phone
                    user.profile.Nic = cnic
                    user.profile.city = city
                    user.profile.country = country
                    user.profile.gender = gender
                    if settings.ENABLE_USER_ACTIVATION:
                        user.is_active = False
                        user.save()
                        user.profile.save()
                        msg = "http://127.0.0.1:8000/activate/"+user.activation_key
                        subject = 'Thank you for registering as a vendor on our site'
                        message = ' Please click this link to verify your account '+msg
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [user.email]
                        send_mail(subject, message, email_from, recipient_list)
                        return redirect('verify')
                    else:
                        user.is_active = True
                        user.save()
                        user.profile.save()
                        return redirect('login')
                else:
                    # user was retrieved
                    errors.append("user already exist. please use some other email")
            except IntegrityError as e:
                errors.append("user already exist. please use some other email")
            
            
        else:
            # request was empty
            errors.append("Please fill the form.")
            
    return render(request, 'pages/vendor/registerVendor.html',{'errors':errors})



def home(requset):
    return render(requset, 'pages/landing.html')

def vendor(request):
    return render(request, 'pages/vendor.html')

def vendor_shop(request):
    errors = []
    if request.method == 'POST':
            name = request.POST.get("name", "")
            first_phone = request.POST.get("first_phone", "")
            second_phone = request.POST.get("second_phone", "")
            status = request.POST.get("status", "")
            Owner = request.user
            form = vendorShop.objects.create(name=name, first_phone=first_phone,second_phone=second_phone,status=status,Owner=Owner)

            form.save()
            return redirect('accountview')
    else:
               # request was empty
        errors.append("Please fill the form.")
    return render(request, 'pages/vendor/vendor_shop.html', {'errors': errors})


def information(request):
   return render(request, 'pages/information.html')

def accountview(request):
   return render(request, 'pages/accountview.html')

def shop_View(request):
   return render(request, 'pages/vendor/shop_view.html')
def shop_edit(request):
    customer = request.user.profile
    form = shopEdit(instance=customer)

    if request.method == 'POST':
        form = shopEdit(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'pages/vendor/shop_edit.html',context)

def shop_details(request):

    return render(request, 'pages/vendor/shop_details.html')

def accountsetting(request):
        customer = request.user.profile
        form = UserForm(instance=customer)

        if request.method == 'POST':
            form = UserForm(request.POST, request.FILES, instance=customer)
            if form.is_valid():
                form.save()

        context = {'form': form}
        return render(request, 'pages/accountsetting.html', context)