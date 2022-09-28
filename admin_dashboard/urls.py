from .views import *
from django.urls import path,include

urlpatterns = [
    path('',admin_dashboard,name='admin-dashboard'),
    path('demo_form',demo_form,name='demo_form')
]
