from django.views import generic
from django.urls import reverse_lazy

from django.contrib.auth import login, authenticate,logout
from django.shortcuts import render, redirect
from .forms import *
from .models import *
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
                return redirect('accountview',username=username)
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


def product_edit(request,id):
    errors = []
    product = Product.objects.get(pk=id)
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get("name", "")
        short_description = request.POST.get("short_description", "")
        long_description = request.POST.get("long_description", "")
        category_id = request.POST.get("category")
        category = Category.objects.filter(id=category_id)
        price = request.POST.get("price", "")
        quantity = request.POST.get("quantity", "")
        Product.objects.filter(pk=id).update(name=name,short_description=short_description,long_description=long_description,price=price,quantity=quantity)
        # if request.FILES:
        #     for f in request.FILES.getlist('images[]'):
        #         print("ok")
        #         image = Images.objects.create(image=f)
        #         product.images.add(image)
        # product.product_categories.add(category)
        shop_id=product.shop.id
        return redirect('shopView',id=shop_id)
        # return HttpResponse("Do something")
    else:
               # request was empty
        categories = Category.objects.all()
        #errors.append("Please fill the form.")
    return render(request, 'pages/product/product_edit.html', {'errors': errors,'categories':categories,'product':product})


def add_product(request,shop_id):
    errors = []
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get("name", "")
        short_description = request.POST.get("short_description", "")
        long_description = request.POST.get("long_description", "")
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)
        price = request.POST.get("price", "")
        quantity = request.POST.get("quantity", "")
        product = Product(name=name,short_description=short_description,long_description=long_description,price=price,quantity=quantity)
        shop = vendorShop.objects.get(id=shop_id)
        product.shop = shop
        product.save()
        print(request.FILES)
        if request.FILES:
            for f in request.FILES.getlist('images[]'):
                print("ok")
                image = Images.objects.create(image=f)
                product.images.add(image)
        product.product_categories.add(category)
        
        return redirect('shopView',id=shop_id)
        # return HttpResponse("Do something")
    else:
               # request was empty
        categories = Category.objects.all()
        #errors.append("Please fill the form.")
    return render(request, 'pages/vendor/add_product.html', {'errors': errors,'categories':categories})

def edit_product(request,edit_id):
    edit=Product.objects.get(id=edit_id)
    form = Edit_Product(instance=edit)

    if request.method == 'POST':
        form = Edit_Product(request.POST, request.FILES, instance=edit)
        if form.is_valid():
            form.save()
           
    context = {'form': form}
    return render(request, 'pages/vendor/Edit_Product.html',context)

def information(request):

def accountview(request,username):
    vendor = User.objects.get(username=username)
    if vendor:
        shops = vendorShop.objects.filter(Owner=vendor)
        return render(request, 'pages/accountview.html',{'vendor':vendor,'shops':shops})
    else:
        return render(request, 'pages/404.html')

def accountEditview(request):
    customer = request.user.profile
    form = UserForm(instance=customer)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'pages/accountsetting.html', context)

def create_shop (request):
    errors = []
    if request.method == 'POST':
        name = request.POST.get("name", "")
        first_phone = request.POST.get("first_phone", "")
        second_phone = request.POST.get("second_phone", "")
        status = "off"
        Owner = request.user
        form = vendorShop.objects.create(name=name, first_phone=first_phone, second_phone=second_phone, status=status,
                                         Owner=Owner)

        form.save()
        return redirect('accountview',username=request.user)
    else:
         # request was empty
         #errors.append("Please fill the form.")
        errors = []
    return render(request, 'pages/vendor/create_shop.html', {'errors': errors})


<<<<<<< HEAD
def shop_View(request,id):
    shop = vendorShop.objects.get(pk=id)
    products = Product.objects.filter(shop=shop)
    return render(request, 'pages/vendor/shop_view.html',{'shop':shop,'products':products})
=======
def shop_View(request,prod_id):
    product = Product.objects.get(id=prod_id)
    print(product)
    context = {'product':product}
    return render(request, 'pages/vendor/shop_view.html',context)
>>>>>>> 641c5edaf0df575c04e46e3ada3ca41193d9e90e

def shop_edit(request,id):
    shop = vendorShop.objects.get(pk=id)

    if request.method == 'POST':
        name = request.POST.get("name", "")
        first_phone = request.POST.get("first_phone", "")
        second_phone = request.POST.get("second_phone", "")
        form = vendorShop.objects.filter(pk=id).update(name=name, first_phone=first_phone, second_phone=second_phone)
        # form.save()
        return redirect('accountview',username=request.user)

    context = {'shop':shop}
    return render(request, 'pages/vendor/shop_edit.html',context)

def shop_details(request,myid):
    vendorshop= vendorShop.objects.get(id=myid)
    print(vendorshop)
    context = {'vendorShop':vendorshop}
    return render(request, 'pages/vendor/shop_details.html',context)

def accountsetting(request):
        customer = request.user.profile
        form = UserForm(instance=customer)

        if request.method == 'POST':
            form = UserForm(request.POST, request.FILES, instance=customer)
            if form.is_valid():
                form.save()

        context = {'form': form}
        return render(request, 'pages/accountsetting.html', context)