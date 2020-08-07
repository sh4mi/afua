from django.urls import path
from . import views
import accounts.views
urlpatterns = [
    path('', accounts.views.home, name='home'),
    path('login/', accounts.views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/user', accounts.views.registerPage, name='register'),
    path('register/vendor', accounts.views.registerVendorPage, name='registerVendor'),
    path('shop/create', accounts.views.create_shop, name='CreateShop'),
    path('shop/view/<int:id>', accounts.views.shop_View, name='shopView'),
    path('shop/edit/<int:id>', accounts.views.shop_edit, name='editShop'),
    path("shop_details/", accounts.views.shop_details, name='detailShop'),


    path('shop/<int:shop_id>/add_product',
         accounts.views.add_product, name='AddProduct'),
    # path('register/contractor', accounts.views.registerContractorPage, name='registerContractor'),
    path('product/edit/<int:id>', accounts.views.product_edit, name='editProduct'),



    path('about-us/', views.about, name='about-us'),
    path('shop/', views.shop, name='shop'),
    path('tobevendor/', views.tobevendor, name='tobevendor'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('information/', accounts.views.information, name='information'),
    path('vendor/', accounts.views.vendor, name='vendor'),
    path('typepaint/', views.typepaint, name='typepaint'),
    # path('accountview/', accounts.views.accountsetting, name='account'),
    path('accountview/<username>', accounts.views.accountview, name='accountview'),
    path('account/edit/',
         accounts.views.accountEditview, name='accountEdit'),

    path('typecement/', views.typecement, name='typecement'),
]
