from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('about-us/', views.about, name='about-us'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('information/', views.information, name='information'),
    path('vendor/', views.vendor, name='vendor'),
    path('typepaint/', views.typepaint, name='typepaint'),
    path('typecement/', views.typecement, name='typecement'),
 ]