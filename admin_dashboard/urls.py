from .views import *
from django.urls import path,include

urlpatterns = [
    path('',admin_dashboard,name='admin-dashboard'),
    path('demo_form',demo_form,name='demo_form'),
    
    path('products_list/',products_list,name='products_list'),
    path('add_product/',add_product,name='add_product')
]
