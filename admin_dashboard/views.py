from django.shortcuts import render
from django.http import HttpResponse
from inventory.models import *

# Create your views here.

def admin_dashboard(request):
    return render(request,'admin_dashboard/admin_base.html')


def demo_form(request):
    return render(request,'admin_dashboard/forms-advanced-form.html')

def products_list(request):
    product_objs=Product.objects.all()
    products_list=[]
    # print('prod objs',product_objs)
    for product_obj in product_objs:
        product_obj_dict=dict()
        product_obj_dict['product']=product_obj
        product_variant_objs=product_obj.product_variants
        product_obj_dict['product_variants']=product_variant_objs.all()
        product_obj_dict['product_cover']=product_variant_objs.first().variant_image.first().image
        product_obj_dict['no_of_variants']=len(product_variant_objs.all())
        product_obj_dict['available_stock']=sum([i.available_stock for i in product_variant_objs.all()])
        product_obj_dict['total_sales']=sum([i.total_sales for i in product_variant_objs.all()])
        print(product_variant_objs.all())
        
        products_list.append(product_obj_dict)

        # print(product_obj_dict)
    context={'page':'Products List','products_list':products_list}
    return render(request,'admin_dashboard/table.html',context)


def add_product(request):
    return render(request,'admin_dashboard/add_product.html')