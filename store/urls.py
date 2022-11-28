from .views import *
from django.urls import path,include

urlpatterns = [
    path('',home,name='home'),
    path('products/',products,name='products'),
    path('product/<str:name>/',single_product,name='single-product'),
    path('cart/',cart,name='cart'),
    path('checkout/',checkout,name='checkout'),

    path('change_product_img_endpoint/<str:v_id>/',change_product_img_endpoint,name='change_product_img_endpoint'),
    path('variant_change_handler_endpoint/<str:v_id>/',variant_change_handler_endpoint,name='variant_change_handler'),
    path('updateCartItem/',updateCartItem,name='updateCartItem'),
    path('removeCartItem/<str:pk>/',removeCartItem,name='remove_cart_item'),
    path('returnCartTotal/',returnCartTotal,name='returnCartTotal'),

    path('get_order_item_endpoint/<str:pk>/',get_order_item_endpoint,name='get_order_item_endpoint'),
]