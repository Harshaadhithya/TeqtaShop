import json
from .models import *
from inventory.models import *
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


from django.db.models import Max
def get_filters():
    filters=dict()
    # categories
    filters['categories']=list(ProductCategory.objects.values_list("name",flat=True)) #we have set unique = true for name field in ProductCategory model so every object in that model has unique name. so we are directly getting all the values from that model without using distinct() function

    # colors
    colors_list=list(ProductVariant.objects.filter(variant_type='color').values_list("variant_name","value"))  #[('red', '#000000'), ('blue', '#0D18ED'), ('blue', '#2CE7FB'), ('blue', '#358BFF'), ('purple', '#834AA6'), ('violet', '#8621C4'), ('red', '#CE2222'), ('red', '#E726B0'), ('red', '#F1225D'), ('red', '#F5E7ED'), ('black', '#FF0000'), ('red', '#FF1256'), ('pink', '#FF3BBE'), ('white', '#FFFFFF')]    
    colors_dict=dict()
    for color_name,color_code in colors_list:
        colors_dict[color_name]=color_code # it has only the unique color names and its value => {'red': '#FF1256', 'blue': '#358BFF', 'purple': '#834AA6', 'violet': '#8621C4', 'black': '#FF0000', 'pink': '#FF3BBE', 'white': '#FFFFFF'}
    filters['colors']=colors_dict
    
    # compatibilty
    compatible_with_list=list(Compatibilty.objects.values_list("name",flat=True))
    filters['compatible_with_list']=compatible_with_list

    # max price
    filters['maxPrice']=ProductVariant.objects.all().aggregate(Max('current_price'))
    print("filters",filters)

    return filters

from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def paginate_products(request,products):
    products_per_page=4
    pages=Paginator(products,products_per_page)
    page_num_range=pages.page_range
    page_no=request.GET.get('page_no')
    if not request.GET.get('page_no'):
        page_no=1
        
    try: 
        products=pages.page(page_no)
    except PageNotAnInteger:
        page_no=1
        products=pages.page(page_no)
    except EmptyPage:
        page_no=len(page_num_range) #this gives the last page no
        products=pages.page(page_no)
    current_page_num = products.number
    has_prev_page = products.has_previous()
    has_next_page = products.has_next()
    has_other_pages = products.has_other_pages()
    previous_page_number = products.previous_page_number
    next_page_number = products.next_page_number

    left_index = int(page_no)-2
    right_index = int(page_no)+2
    if left_index < 1:
        left_index = 1
    if right_index > len(page_num_range):
        right_index = len(page_num_range)
    custom_page_num_range = range(left_index,right_index+1)

    context2={'page_num_range':page_num_range,'current_page_num':current_page_num,'has_prev_page':has_prev_page,'has_next_page':has_next_page,'has_other_pages':has_other_pages,'previous_page_number':previous_page_number,'next_page_number':next_page_number,'custom_page_num_range':custom_page_num_range,'last_page_num':len(page_num_range),'last_page_num_minus_1':len(page_num_range)-1}

    return products,context2