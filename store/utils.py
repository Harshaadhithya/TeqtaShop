import json
from .models import *
from .serializers import *

def cookieCart(request):
    print("utils working")
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
        try: #this try except is used because for guestcart, it remains until the cokkie or cache is removed, what if i delete some product at admin side and if a guest user tries to view his cart then no product matching query error will be shown, to avoid that we use try catch here
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

        except:
            pass
    return {'items': items, 'order': order, 'cart_total_qty': cart_total_qty}


def cartData(request):
    print("utils1 working")
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_total_qty = order.get_cart_qty_total
    else:
        cookieData=cookieCart(request)
        items=cookieData['items']
        order=cookieData['order']
        cart_total_qty=cookieData['cart_total_qty']

    return {'items': items, 'order': order, 'cart_total_qty': cart_total_qty}