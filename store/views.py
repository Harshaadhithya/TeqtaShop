import imp
from itertools import product
from logging import exception
from multiprocessing import context
from tkinter.messagebox import NO
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from inventory.models import *
import json
from .models import *
from django.contrib import messages

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *

from admin_dashboard.templatetags.custom_tags import get_cart_total_qty
from .forms import *
from django.db.models import Q

from .utils import *


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


def get_guest_cart_detail(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
        # we get cookie cart as a string, so we are using json.loads to ocnvert it in to dict object
    except:
        # whenever there is no cart cookie, then it may raise an error here, so empty dict is assigned to cart
        cart = {}
    
    order = {'id':'guest_id','get_cart_total': 0, 'get_cart_qty_total': len(cart)}
    items = []
    cart_total_qty = order['get_cart_qty_total']

    for i in cart:
        product = ProductVariant.objects.get(id=i)
        # print("cart total",order['get_cart_total'],"+",product.current_price * cart[i]['quantity'],"=",product.current_price * cart[i]['quantity']+order['get_cart_total'])
        item_total=product.current_price * cart[i]['quantity']
        order['get_cart_total'] += item_total
        
        # item = {
        #     'id':product.id,
        #     'product':{
        #         'id':product.id,
        #         'product':{'name':product.product.name},
        #         'current_price':product.current_price,
        #         'variant_name':product.variant_name,
        #         'variant_image':{
        #             'first':{'image':{'url':product.variant_image.first().image.url}}
        #             },
                
        #         },
        #     'quantity':cart[i]['quantity'],
        #     'get_total':order['get_cart_total'],
        # }
        item = {
            'id':product.id,
            'product':product,
            'quantity':cart[i]['quantity'],
            'get_total':item_total,
        }
        serialized_item=GuestCartSerializer(item).data
        
        print(json.dumps(serialized_item),"\n\n")
        items.append((serialized_item))

    return JsonResponse({'items':items,'order':order,'cart_total_qty':cart_total_qty})
        

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

@api_view(['GET'])
def api_test(request,pk):
    # product_variant_obj=ProductVariant.objects.get(id=pk)
    # data1={'id':pk,'product':product_variant_obj}
    # serialized_product_variant=TestSerializer(data1).data
    # return Response(serialized_product_variant)
    return JsonResponse({})

def home(request):
    products = Product.objects.filter().order_by('-created')[:12]
    print(products)
    for product in products:
        print(product.product_variants.first().variant_image.first().image.url)
    context = {'page_title': 'home_page', 'products': products}
    # messages.success(request,"test message")
    return render(request, 'store/index.html', context)


def products(request):
    search_query=request.GET.get('search_query')
    if search_query==None:
        search_query=''
    
    products=Product.objects.distinct().filter(
        Q(name__icontains=search_query) | Q(tags__name__icontains=search_query) | Q(category__name__icontains=search_query)
    )
    context = {'page_title': 'products_page','products': products,'search_query':search_query,'result_length':len(products)}
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
    # if request.user.is_authenticated:
    #     customer = request.user.profile
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all()
    #     cart_total_qty = order.get_cart_qty_total
    # else:
    #     cookieData=cookieCart(request)
    #     items=cookieData['items']
    #     order=cookieData['order']
    #     cart_total_qty=cookieData['cart_total_qty']
        
    data=cartData(request)
    items=data['items']
    order=data['order']
    cart_total_qty=data['cart_total_qty']

    context = {'items': items, 'order': order, 'cart_total_qty': cart_total_qty}
    return render(request, 'store/cart-page.html', context)


def checkout(request):
    data=cartData(request)
    items=data['items']
    order=data['order']
    shippingForm=ShippingForm()
    context = {'items': items, 'order': order, 'shippingForm':shippingForm}
    if request.user.is_authenticated:
        customer=request.user.profile
        context['customer']=customer

    
    # if request.method == 'POST':
    #     if shippingForm.is_valid():
    #         shippingAddress=shippingForm.save(commit=False)
    #         shippingAddress.order=order
    #         shippingAddress.customer=request.user.profile
    #         shippingAddress.save()
    #         return redirect('process_order')
            # check for the above else where order_id is not included
    
    return render(request, 'store/checkout.html', context)

def process_order(request):
    if request.method == 'POST':
        shippingForm=ShippingForm(request.POST)
        if request.user.is_authenticated:
            customer=request.user.profile
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        else:
            cookieData=cookieCart(request)
            print("cookiedata\n",cookieData)
            items=cookieData['items']
            
            
            customer,created=Profile.objects.get_or_create(email=request.POST['email'],mobile=request.POST['mobile'])
            customer.first_name=request.POST['first_name']
            customer.last_name=request.POST['last_name']
            customer.mobile=request.POST['mobile']
            customer.save()
            print("custom",customer)
            order=Order.objects.create(customer=customer,complete=False)
            # for guest orders, we should not use get_or_create by seeing cutomer and complete fields, because sometimes the cookie cart maybe cleared now new cart will be created and the user wants to buy the new cart items, so if we use old orders it will also include old products from old orders.
            for item in items:
                product=ProductVariant.objects.get(id=item['id'])
                order_item=OrderItem.objects.create(order=order,product=product,quantity=item['quantity'])

                
        if shippingForm.is_valid():
            print("insisde if")
            shipping_form=shippingForm.save()
            shipping_form.order=order
            shipping_form.customer=customer
            shipping_form.save()
        # refer 1hr at video
            total=order.get_cart_total
            # payment logic
            order.complete=True
            order.save()
            messages.success(request,'Order Processing')
            # cart should be emptied after transaction is successfull
        else:
            print("inside else",shippingForm.errors)
            messages.warning(request,"Something went wrong!")
            return redirect('checkout')

    
    return redirect('home')

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


# for logged in users
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

    # only if the product has available stocks then orderitem is saved else it returns with an out of stock msg without updating(refer prev line)
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