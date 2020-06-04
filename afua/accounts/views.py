from django.views import generic
from django.urls import reverse_lazy

from django.contrib.auth import login, authenticate,logout
from django.shortcuts import render, redirect

import uuid
from django.core.mail import send_mail

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()

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
            return render(request, 'pages/login2.html', context)
     else:
      context = {}
     return render(request, 'pages/login2.html', context)

def logoutUser(request):
        logout(request)
        return redirect('login')

# Create your views here.
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


def registerVendorPage(request):
    errors = []
    if request.method == 'POST':
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        password = request.POST.get("password", "")
        # country = request.POST.get("country", "")
        if email and username and password and phone :
            try:
                user,created = User.objects.get_or_create(username=username, email=email)
                if created:
                    # user.user_type=3
                    user.user_type = 'vendor'
                    user.set_password(password)
                    user.activation_key = uuid.uuid4().hex[:30]
                    user.profile.phone = phone
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




def vendor(request):
    return render(request, 'pages/vendor.html')


def information(request):
   return render(request, 'pages/information.html')
