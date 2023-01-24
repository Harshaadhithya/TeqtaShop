from django import template
from store.models import *
import json

register = template.Library()

@register.simple_tag(name = 'get_list_ele')
def get_list_ele(value,index):
    return value[int(index)]

# register.filter('get_list_ele', get_list_ele)

from django import template
register = template.Library()

@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return qty * (unit_price)

@register.simple_tag()
def get_cart_total_qty(request,*args, **kwargs):
    if request.user.is_authenticated:
        customer=request.user.profile
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        print("creating here")
        total=order.get_cart_qty_total
        # items=order.orderitem_set.all()
    else:  
        try:
            cart = json.loads(request.COOKIES['cart'])
            # we get cookie cart as a string, so we are using json.loads to ocnvert it in to dict object
        except:
            # whenever there is no cart cookie, then it may raise an error here, so empty dict is assigned to cart
            cart = {}
        # order = {'get_cart_total': 0, 'get_cart_qty_total': 0}
        total=len(cart)
    return total

    
