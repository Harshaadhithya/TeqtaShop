import imp
from itertools import product
from logging import exception
from multiprocessing import context
from tkinter.messagebox import NO
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from inventory.models import *
import json
from .models import *
from django.contrib import messages

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *

from admin_dashboard.templatetags.custom_tags import get_cart_total_qty


# Create your views here.

def get_cart_detail(request, msg=None):
    customer = request.user.profile
    # product = ProductVariant.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    serialized_order = OrderSerializer(order, many=False).data
    augmented_serializer_data = serialized_order
    augmented_serializer_data['msg'] = msg
    # print(augmented_serializer_data)
    return JsonResponse(augmented_serializer_data)


@api_view(['GET'])
def get_order_item_endpoint(request, pk):
    msg = 'updated'

    if pk == 'null':
        msg = 'deleted'
    else:
        msg = 'updated'
    # order_item=OrderItem.objects.get(id=pk)
    # order_obj=order_item.order
    # serialized_order=OrderSerializer(order_obj,many=False).data
    # augmented_serializer_data = serialized_order
    # augmented_serializer_data['msg']= msg
    cart = get_cart_detail(request, msg)
    print("cart", cart, "\n", type(cart))
    return cart


def home(request):
    products = Product.objects.filter().order_by('-created')[:12]
    print(products)
    for product in products:
        print(product.product_variants.first().variant_image.first().image.url)
    context = {'page_title': 'home_page', 'products': products}
    # messages.success(request,"test message")
    return render(request, 'store/index.html', context)


def products(request):
    context = {'page_title': 'products_page'}
    return render(request, 'store/products.html', context)


def change_product_img_endpoint(request, v_id):
    try:
        variant_obj = ProductVariant.objects.get(id=v_id)
        variant_img_obj = variant_obj.variant_image.first()
        image_url = variant_img_obj.image.url
        offer_obj = variant_obj.product.offer
        if offer_obj == None:
            offer = None

        else:
            offer = {'percentage': offer_obj.percentage}

        product_detail_dict = {'name': variant_obj.product.name, 'original_price': variant_obj.original_price,
                               'current_price': variant_obj.current_price, 'offer': offer}
        return JsonResponse({'status': 'success', 'image_url': image_url, 'product': product_detail_dict})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'failed'})


def single_product(request, name):
    product = Product.objects.get(name=name)
    product_variants = product.product_variants.all()
    context = {'product': product, 'product_variants': product_variants}
    return render(request, 'store/single-product.html', context)


def cart(request):
    # context={}
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        order = {'get_cart_total': 0, 'get_cart_qty_total': 0}
        items = []
    cart_total_qty = order.get_cart_qty_total
    context = {'items': items, 'order': order, 'cart_total_qty': cart_total_qty}
    return render(request, 'store/cart-page.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        order = {'get_cart_total': 0, 'get_cart_qty_total': 0}
        items = []
    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)


def variant_change_handler_endpoint(request, v_id):
    variant_obj = ProductVariant.objects.get(id=v_id)
    variant_img_objs = variant_obj.variant_image.all()
    variant_img_urls = [variant_img_obj.image.url for variant_img_obj in variant_img_objs]
    offer_obj = variant_obj.product.offer
    description = variant_obj.description
    if description == '':
        description = variant_obj.product.description
    if offer_obj == None:
        offer = None

    else:
        offer = {'percentage': offer_obj.percentage}
    product_dict = {'variant_id': variant_obj.id, 'original_price': variant_obj.original_price,
                    'current_price': variant_obj.current_price, 'offer': offer,
                    'available_stock': variant_obj.available_stock, 'description': description}
    print(product_dict)
    return JsonResponse({'status': 'success', 'variant_img_urls': variant_img_urls, 'product': product_dict,
                         'product_id': variant_obj.product.id})


def get_cart(request):
    customer = request.user.profile
    # product = ProductVariant.objects.get(id=productId)
    order_obj = Order.objects.get(customer=customer, complete=False)
    serialized_order = OrderSerializer(order_obj, many=False).data
    # augmented_serializer_data = serialized_order
    # augmented_serializer_data['status']= 'test'
    return Response(serialized_order)


def updateCartItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(action, productId)
    customer = request.user.profile
    product = ProductVariant.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    order_item_id = orderItem.id

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    print(product.available_stock - orderItem.quantity)
    if product.available_stock - orderItem.quantity < 0:
        return JsonResponse(
            {'status': 'not_updated', 'message': 'out of stock', 'detail_msg': f'{product} is out of stock !!',
             'msg_tag': 'warning', 'order_item_id': order_item_id})

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
        order_item_id = None

        return JsonResponse({'status': 'updated', 'message': 'Item was Deleted', 'order_item_id': order_item_id})

    return JsonResponse({'status': 'updated', 'message': 'Item was added', 'order_item_id': order_item_id})


def removeCartItem(request, pk):
    try:
        order_item = OrderItem.objects.get(id=pk)
        order_item.delete()
        # cart_tota_qty=get_cart_total_qty(request)
        # print(cart_tota_qty,"cart_total")
        # return JsonResponse({'message':'success','cart_total_qty':cart_tota_qty})
        cart = get_cart_detail(request, msg="success")
        return cart

    except Exception as e:
        print(e)
        return JsonResponse({'message': 'failed'})


def returnCartTotal(request):
    total = get_cart_total_qty(request)
    print("totoal", total)
    return JsonResponse({'cart_total_qty': total})