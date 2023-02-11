from .views import *
from django.urls import path,include

urlpatterns = [
    path('',admin_dashboard,name='admin-dashboard'),
    path('demo_form',demo_form,name='demo_form'),
    
    path('products_list/',products_list,name='products_list'),
    path('add_product/',add_product,name='add_product'),
    path('edit_product/<str:pk>/',edit_product,name='edit_product'),

    path('inventory/',inventory,name='inventory'),
    path('edit_variant/<str:pk>/',edit_variant,name='edit_variant'),

    path('collections/',collections,name='collections'),
    path('add_collection/',add_collection,name='add_collection'),
    path('edit_collection/<str:pk>/',edit_collection,name='edit_collection'),
    path('delete_collection/<str:pk>/',delete_collection,name='delete_collection'),

    path('offers/',offers,name='offers'),
    path('add_offer/',add_offer,name='add_offer'),
    path('edit_offer/<str:pk>/',edit_offer,name='edit_offer'),
    path('delete_offer/<str:pk>/',delete_offer,name='delete_offer'),

    path('update_stock_endpoint/',update_stock_endpoint,name='update_stock_endpoint'),
    path('delete_img_endpoint/<str:pk>/',delete_img_endpoint,name='delete_img_endpoint'),
    path('view_collection_products_endpoint/<str:pk>/',view_collection_products_endpoint,name='view_collection_products_endpoint'),
    path('remove_product_from_collection/<str:c_id>/<str:p_id>/',remove_product_from_collection,name='remove_product_from_collection'),

    path('coupons/',coupons,name='coupons'),
    path('add_coupon/',add_coupon,name='add_coupon'),
    path('edit_coupon/<str:pk>/',edit_coupon,name='edit_coupon'),
    path('view_coupon_products_endpoint/<str:pk>/',view_coupon_products_endpoint,name='view_coupon_products_endpoint'),
    path('remove_product_from_coupon/<str:c_id>/<str:p_id>/',remove_product_from_coupon,name='remove_product_from_coupon'),



   

    path('check/',check,name='check'),
    # path('test_data/',test_data,name='test_data')
]
