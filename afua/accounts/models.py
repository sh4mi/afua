from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models.signals import post_save
import uuid
import os

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
    Owner = models.ForeignKey(User, on_delete=models.CASCADE )
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

# all category will created here first

def get_image_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('', filename)


class Images(models.Model):
    image = models.ImageField(upload_to=get_image_filename,null=True,blank=True,default="product_placeholder.jpg",
                            verbose_name='product_image')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    # unique name constraint in name

    def __str__(self):
        return self.name

# this is the relationship model between categories
# category is the foreign key
# children -> one category can have many categories.


class Categories(models.Model):
    category = models.OneToOneField(
        Category, on_delete=models.CASCADE, related_name='category_obj')
    children = models.ManyToManyField(Category)

    def __str__(self):
        return self.category.name
    # this function is linked with category. so that when any category is created we can store its children inside it.
    # when new category created this function will called and create a empty relation ship with category model with zero children. but we can add multple childrens later.

    def create_profile(sender, **kwargs):
        category = kwargs["instance"]
        if kwargs["created"]:
            category_profile = Categories(category=category)
            category_profile.save()
    post_save.connect(create_profile, sender=Category)





class Product(models.Model):
    shop = models.ForeignKey(vendorShop, on_delete=models.CASCADE )
    name = models.CharField(max_length=20, blank=True, default='')
    short_description = models.CharField(max_length=220, blank=True, default='')
    long_description = models.TextField(blank=True, default='')
    product_categories = models.ManyToManyField(Category)
    images = models.ManyToManyField(Images,related_name="product_image")
    price = models.IntegerField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

