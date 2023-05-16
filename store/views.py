import decimal
import imp
from itertools import product
from logging import exception
from multiprocessing import context
from tkinter.messagebox import NO
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
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
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


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
    filters=get_filters()
    if search_query==None:
        search_query=''
    
    products=Product.objects.distinct().filter(
        Q(name__icontains=search_query) | Q(tags__name__icontains=search_query) | Q(category__name__icontains=search_query)
    )
    products,context2 = paginate_products(request,products=products)
    context = {'page_title': 'products_page','products': products,'search_query':search_query,'result_length':len(products),'filters':filters}
    combined_context = {**context,**context2}
    return render(request, 'store/products.html', combined_context)


def filter_products(request):
    search_query=request.GET.get('search_query')
    filters=get_filters()
    colors=[]
    compatiblity=[]
    categories=[]
    if search_query==None:
        search_query=''
    
    if request.method=='POST':
        selected_filters=json.loads(request.POST.get('selected_filters'))
        colors=selected_filters['color']
        compatiblity=selected_filters['compatibility']
        categories=selected_filters['category']

        maxPrice = selected_filters['maxPrice']
        print(type(maxPrice),maxPrice)
        
    # all_products=Product.objects.all()
    all_products = Product.objects.distinct().filter(
        Q(name__icontains=search_query) | Q(tags__name__icontains=search_query) | Q(category__name__icontains=search_query)
    )
    if maxPrice!='' or maxPrice!=None:
        all_products=all_products.filter(product_variants__current_price__lte=int(maxPrice)).distinct()   
    if len(colors)>0:
        print("colo",colors)
        all_products=all_products.filter(product_variants__variant_name__in=colors).distinct()
    if len(compatiblity)>0:
        all_products=all_products.filter(product_variants__compatible_with__name__in=compatiblity).distinct()
    if len(categories)>0:
        all_products=all_products.filter(category__name__in=categories).distinct()

    all_products,context2 = paginate_products(request,all_products)

    template = render_to_string('store/filtered-products-list.html',{'products':all_products,'search_query':search_query,'result_length':len(all_products)}) #render_to_string turns the template into a string and stores it in this template variable
    pagination_template = render_to_string('store/pagination.html',context2)

    return JsonResponse({'template_text':template,'pagination_template':pagination_template}) #the template which is converted into string is passed as a response

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
    # print(get_filters())
    
    categories=product.category.all()
    tags=product.tags.all()
    # print(categories_list)
    recommended_products = Product.objects.distinct().filter(Q(category__in=categories) | Q(tags__in=tags)).exclude(id=product.id)[:8]
    if(len(recommended_products)<8): 
        # 8 is the maximum number of products that can be showned in recommended products section , so to ensure whether 8 products are displayed
        difference=8-len(recommended_products)
        extra_products=Product.objects.filter().exclude(Q(id__in=[rec_product.id for rec_product in recommended_products]) | Q(id=product.id)) #here we are excluding the products that are in recommended products and excluding the current product also
        extra_products=extra_products[:difference]
        recommended_products = recommended_products | extra_products #combining both the querysets
    
    # print(recommended_products)
    context = {'product': product, 'product_variants': product_variants,'recommended_products':recommended_products}
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

    # print("items",items)
    # recommended products
    
    recommended_products = products_recommendation(request,items)
    
    context = {'items': items, 'order': order, 'cart_total_qty': cart_total_qty,'recommended_products':recommended_products}
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


from itertools import chain
from django.core.exceptions import ObjectDoesNotExist

def apply_coupon(request):
    coupon_code = request.POST.get("coupon_code")
    data=cartData(request)
    items=data['items']
    order=data['order']
    try:
        coupon_obj = Coupon.objects.get(name = coupon_code,status='Active')
        # print(cartData(request))
        
        print("items",items)
        if not request.user.is_authenticated:
            items_id_list=[item.id for item in items]
            product_variants_list=[ProductVariant.objects.get(id=prod_var_id) for prod_var_id in items_id_list]
            
            print("prodvarlist",product_variants_list)
            discount_dict = {prod_var.product:0 for prod_var in product_variants_list}
        else:
        # test_dict={order_item.product.product:type(order_item.product.product) for order_item in items}
        # if request.user.is_authenticated:
            discount_dict = {order_item.product.product:0 for order_item in items} #the key will be unique products, not product variants. if i have iphone-blue and iphone-purple in my cart, then this dict has only one key coresponding to both that product variants which is the product object(iphone)
        coupon_applicable_products = coupon_obj.applicable_products.all()
        # else:
        #     discount_dict = {order_item.product.product.name:0 for order_item in items} #the key will be unique products, not product variants. if i have iphone-blue and iphone-purple in my cart, then this dict has only one key coresponding to both that product variants which is the product object(iphone)
        #     coupon_applicable_products = [product.name for product in coupon_obj.applicable_products.all()]
        print("coupon_applicable produts",coupon_applicable_products)
        
        print("dis dict",discount_dict)
        # print("test dict",test_dict)

        # if request.user.is_authenticated:
        for product,discount in discount_dict.items():
            if product in coupon_applicable_products:
                print("prodddd",product)
                total_price=0  #this variable is going to hold the total price for each key(product) in discount dict. if i have both iphone-blue and iphone-purple in my cart then these both variants belongs to the same key(iphone) and the total_proce variable computes and adds the price of both variants and stores it in this single variable
                
                print("items",items)
                if not request.user.is_authenticated:
                    product_variants_in_order_items = [prod_var for prod_var in product_variants_list if prod_var.product==product] #we can only use .filter in querysets, but here we have a list of objects not a queryset, so we use list comprehension to filter the product variants that belongs the current product in this loop
                    print("currprod",product,"\nprodvars",product_variants_in_order_items,"\n\n")
                    for prod_var in product_variants_in_order_items:
                        print('provarid',prod_var.id,prod_var.product.name,prod_var.variant_name)
                        # print([item["id"] for item in items if int(item["id"])==prod_var.id])
                        total_price+=sum([decimal.Decimal(item.get_total) for item in items if int(item.id)==prod_var.id])
                        # print("tot pri",total_price)
                        # 
                    # total_price=sum([prod_var.id for prod_var in product_variants_in_order_items])
                else:
                    product_variants_in_order_items = items.filter(product__product=product)  #this is executed in a for lopp which iterates over each key, f the key is iphone then it filters all the orderitems that has the product iphone, it returns iphone-blue and iphone-purple in this case
                    for order_item in product_variants_in_order_items:
                        total_price+=order_item.get_total
                print("filtered",product_variants_in_order_items)
                print(product,"=",total_price)

                if coupon_obj.coupon_type == 'percentage':
                    print("percentage")
                    discount = round(decimal.Decimal(coupon_obj.value/100)*total_price)
                    if discount < total_price:
                        discount_dict[product] = discount
                elif coupon_obj.coupon_type == 'cashback':
                    if coupon_obj.value < total_price:  #this is checked to enesure whether the total price for the product is greater than the cashback. if total price of product =10 but cashback is 15 then the discounted prices will be -5 which is negative
                        # discount+=coupon_obj.value
                        discount_dict[product] = coupon_obj.value
                    print("cashback",coupon_obj.value)
                else:
                    pass
                print("dis dict",discount_dict)
            else:
                pass
                print(product,"not in list")
            
        # else:
        #     pass
        
        total_discount=sum(discount_dict.values())
        if not request.user.is_authenticated:
            discounted_order_total = order['get_cart_total']-decimal.Decimal(total_discount)
        else:
            discounted_order_total = order.get_cart_total-decimal.Decimal(total_discount)
        
        checkout_card_template = render_to_string('store/checkout-card.html',context={'items':items,'order':order,"discount":total_discount,"discounted_order_total":discounted_order_total,'coupon_code':coupon_code,'status':'success'})

    except ObjectDoesNotExist:
        print("does not exist")
        data=cartData(request)
        context={'items':items,'order':order,'discount':None,'discounted_order_total':None,'coupon_code':coupon_code,'status':'failed'}
        checkout_card_template = render_to_string('store/checkout-card.html',context)
        return JsonResponse({"status":"failed","msg":f"Coupon '{coupon_code}' does not exist","checkout_card_template":checkout_card_template})

    except Exception as e:
        data=cartData(request)
        context={'items':items,'order':order,'discount':None,'discounted_order_total':None,'coupon_code':coupon_code,'status':'failed'}
        checkout_card_template = render_to_string('store/checkout-card.html',context)

        print(e.__class__.__name__)
        return JsonResponse({"status":"failed","msg":"Something went wrong","checkout_card_template":checkout_card_template})
    return JsonResponse({"coupon_code":request.POST.get("coupon_code"), "discount":total_discount, "checkout_card_template":checkout_card_template})


# use tis function if we use serialized cartdata for unauthenticated users
"""
def apply_coupon(request):
    coupon_code = request.POST.get("coupon_code")
    try:
        coupon_obj = Coupon.objects.get(name = coupon_code,status='Active')
        print(cartData(request))
        data=cartData(request)
        items=data['items']
        order=data['order']
        print("items",items)
        if not request.user.is_authenticated:
            items_id_list=[item["id"] for item in items]
            product_variants_list=[ProductVariant.objects.get(id=prod_var_id) for prod_var_id in items_id_list]
            
            # print("items id",items_id_list)
            discount_dict = {prod_var.product:0 for prod_var in product_variants_list}
        else:
            discount_dict = {order_item.product.product:0 for order_item in items} #the key will be unique products, not product variants. if i have iphone-blue and iphone-purple in my cart, then this dict has only one key coresponding to both that product variants which is the product object(iphone)
        coupon_applicable_products = coupon_obj.applicable_products.all()
        print(coupon_applicable_products)
        
        print("dis dict",discount_dict)

        # if request.user.is_authenticated:
        for product,discount in discount_dict.items():
            if product in coupon_applicable_products:
                total_price=0  #this variable is going to hold the total price for each key(product) in discount dict. if i have both iphone-blue and iphone-purple in my cart then these both variants belongs to the same key(iphone) and the total_proce variable computes and adds the price of both variants and stores it in this single variable
                
                print("items",items)
                if not request.user.is_authenticated:
                    product_variants_in_order_items = [prod_var for prod_var in product_variants_list if prod_var.product==product] #we can only use .filter in querysets, but here we have a list of objects not a queryset, so we use list comprehension to filter the product variants that belongs the current product in this loop
                    for prod_var in product_variants_in_order_items:
                        print('provarid',prod_var.id)
                        print([item["id"] for item in items if int(item["id"])==prod_var.id])
                        total_price+=sum([decimal.Decimal(item["get_total"]) for item in items if int(item["id"])==prod_var.id])
                        # print("tot pri",total_price)
                        # 
                    # total_price=sum([prod_var.id for prod_var in product_variants_in_order_items])
                else:
                    product_variants_in_order_items = items.filter(product__product=product)  #this is executed in a for lopp which iterates over each key, f the key is iphone then it filters all the orderitems that has the product iphone, it returns iphone-blue and iphone-purple in this case
                    for order_item in product_variants_in_order_items:
                        total_price+=order_item.get_total
                print("filtered",product_variants_in_order_items)
                
                print(product,"=",total_price)

                if coupon_obj.coupon_type == 'percentage':
                    print("percentage")
                    discount = round(decimal.Decimal(coupon_obj.value/100)*total_price)
                    if discount < total_price:
                        discount_dict[product] = discount
                elif coupon_obj.coupon_type == 'cashback':
                    if coupon_obj.value < total_price:  #this is checked to enesure whether the total price for the product is greater than the cashback. if total price of product =10 but cashback is 15 then the discounted prices will be -5 which is negative
                        # discount+=coupon_obj.value
                        discount_dict[product] = coupon_obj.value
                    print("cashback",coupon_obj.value)
                else:
                    pass
                print("dis dict",discount_dict)
            else:
                pass
                print(product,"not in list")
            
        # else:
        #     pass
        
        total_discount=sum(discount_dict.values())
        if not request.user.is_authenticated:
            discounted_order_total = order['get_cart_total']-decimal.Decimal(total_discount)
        else:
            discounted_order_total = order.get_cart_total-decimal.Decimal(total_discount)
        
        checkout_card_template = render_to_string('store/checkout-card.html',context={'items':items,'order':order,"discount":total_discount,"discounted_order_total":discounted_order_total,'coupon_code':coupon_code})

    except Exception as e:
        print(e)
        return JsonResponse({"status":"failed","msg":f"Coupon '{coupon_code}' does not exist"})
    return JsonResponse({"coupon_code":request.POST.get("coupon_code"), "discount":total_discount, "checkout_card_template":checkout_card_template})
"""