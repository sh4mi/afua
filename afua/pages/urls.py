from django.urls import path
from . import views
import accounts.views
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', accounts.views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/user', accounts.views.registerPage, name='register'),
    path('register/vendor', accounts.views.registerVendorPage, name='registerVendor'),
    # path('register/contractor', accounts.views.registerContractorPage, name='registerContractor'),
    path('about-us/', views.about, name='about-us'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('information/', accounts.views.information, name='information'),
    path('vendor/', accounts.views.vendor, name='vendor'),
    path('typepaint/', views.typepaint, name='typepaint'),
    path('typecement/', views.typecement, name='typecement'),
 ]