import decimal
from importlib.resources import path
from math import prod
from multiprocessing import context
from sys import prefix
from django.shortcuts import render,redirect
from django.http import HttpResponse
from inventory.models import *
from .forms import *
from django.contrib import messages

# Create your views here.

def admin_dashboard(request):
    return render(request,'admin_dashboard/admin_base.html')


def demo_form(request):
    return render(request,'admin_dashboard/forms-advanced-form.html')

def update_offer_price(product,offer):
    product_variants=product.product_variants.all()
    if offer==None:
        for product_variant_obj in product_variants:
            product_variant_obj.current_price=product_variant_obj.original_price
            product_variant_obj.save()
    else:
        for product_variant_obj in product_variants:
            offer_price=(product_variant_obj.original_price)-(decimal.Decimal(offer.percentage/100)*product_variant_obj.original_price)
            product_variant_obj.current_price=offer_price
            product_variant_obj.save()

    

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
        # print(product_variant_objs.all())
        
        products_list.append(product_obj_dict)

        # print(product_obj_dict)
    context={'page':'Products List','products_list':products_list}
    return render(request,'admin_dashboard/table.html',context)


from django.forms import modelformset_factory
from django.forms import inlineformset_factory


def add_product(request):
    product_form=AddProductForm()
    product_variant_form=ProductVariantFullForm(prefix='product_variant_form')
    product_variant_formset=modelformset_factory(ProductVariant,
                                        form=ProductVariantFullForm, extra=10,can_delete=True)
    i_pv_formset=inlineformset_factory(Product,ProductVariant,form=ProductVariantFullForm,extra=10, can_delete=True)
    formset1=i_pv_formset(queryset=ProductVariant.objects.none())
    formset = product_variant_formset(queryset=ProductVariant.objects.none())
    if request.method=='POST':
        post=request.POST.copy()
        tag_list=[]
        for tag_id in request.POST.getlist('tags'):
            print(tag_id)
            try:
                if ProductTag.objects.filter(id=tag_id).exists(): #if this arises any error then there exist no such tag, this error is arised because we will be getting id if already tag is exist, else we will get the name of the new tag entered and when we try to match with tag id it causes an error.
                    pass
                
                else:
                    tag_obj=ProductTag.objects.create(name=tag_id)
                    tag_id=tag_obj.id

            except:
                tag_obj=ProductTag.objects.create(name=tag_id)
                tag_id=tag_obj.id
            tag_list.append(tag_id)
            print("taglist",tag_list)

        post.setlist('tags', tag_list)

        badge_list=[]
        print("badge post",request.POST.getlist('badge'))
        for badge_id in request.POST.getlist('badge'):
            print("batch_id",badge_id)
            if badge_id!='':
                try:
                    if SpecialBadge.objects.filter(id=badge_id).exists(): #if this arises any error then there exist no such tag, this error is arised because we will be getting id if already tag is exist, else we will get the name of the new tag entered and when we try to match with tag id it causes an error.
                        pass
                    
                    else:
                        badge_obj=SpecialBadge.objects.create(name=badge_id)
                        badge_id=badge_obj.id

                except:
                    badge_obj=SpecialBadge.objects.create(name=badge_id)
                    badge_id=badge_obj.id
                badge_list.append(badge_id)
                print("badgelist",badge_list)

            post.setlist('badge', badge_list)

        category_list=[]
        for category_id in request.POST.getlist('category'):
            if category_id!='':
                try:
                    if ProductCategory.objects.filter(id=category_id).exists():
                        pass
                    else:
                        category_obj=ProductCategory.objects.create(name=category_id)
                        category_id=category_obj.id
                except:
                    category_obj=ProductCategory.objects.create(name=category_id)
                    category_id=category_obj.id
                category_list.append(category_id)
            post.setlist('category',category_list)

        request.POST=post
        print(request.POST['tags'],request.POST)
        print(request.POST["badge"])

        
        product_form=AddProductForm(request.POST)
        print(product_form.errors)
        if product_form.is_valid():
            print("inisde first valid")
            product_obj=product_form.save()
            formset1=i_pv_formset(request.POST,request.FILES,instance=product_obj,queryset=ProductVariant.objects.none())
            # print("formset1",formset1)
            for index,form in enumerate(formset1):
                all_product_variant_objs=[]
                all_varaint_img_objs=[]
                if form.is_valid():
                    # try:
                    product_variant_obj=form.save()
                    all_product_variant_objs.append(all_product_variant_objs)

                    images=request.FILES.getlist(f'product_variants-{index}-images')
                    if len(images) < 1:
                        messages.warning(request,f"{product_variant_obj.product.name} should have atleast 1 Image !!")
                        # delete product obj, all product variant objs and image objs
                        # return redirect

                    print("images",images)
                    for image in images:
                        variant_image_obj=ProductImage.objects.create(product_variant=product_variant_obj,image=image)
                        all_varaint_img_objs.append(variant_image_obj)
                        print("image saved")
                    # except:
                    #     # capture exception
                    #     print("exception occured")
                    #     for each_obj in all_product_variant_objs:
                    #         each_obj.delete()
                    #     for each_obj in all_varaint_img_objs:
                    #         each_obj.delete()
                    #     product_obj.delete()
                    #     context={'product_form':product_form,'formset':formset,'formset1':formset1}
                    #     messages.error(request,"Something went wrong !!")
                    #     return render(request,'admin_dashboard/add_product1.html',context)
                else:
                    if form.non_field_errors():
                        print("yes non field error",form.non_field_errors)
                        for error in form.non_field_errors():
                            print("non field error",error)
                            messages.error(request,f"{error}")
                        # for each_obj in all_product_variant_objs:
                        #     each_obj.delete()
                        # for each_obj in all_varaint_img_objs:
                        #     each_obj.delete()
                        # product_obj.delete()
                        
                        # context={'product_form':product_form,'formset':formset,'formset1':formset1}
                        # return render(request,'admin_dashboard/add_product1.html',context)
                        # return redirect('add_product')
                    print(f'form-{index+1} not valid')
                    
            messages.success(request,"Product Added Successfully !!")
            return redirect('products_list')
        else:
            messages.error(request,"Unable to add this product !!")
        

    context={'product_form':product_form,'formset':formset,'formset1':formset1}
    return render(request,'admin_dashboard/add_product1.html',context)



def edit_product(request,pk):
    context={}
    product_obj=Product.objects.get(id=pk)
    product_form=AddProductForm(instance=product_obj)
    product_variant_objs=product_obj.product_variants.all()
    prefilled_variant_forms_list=[]
    list_of_variant_image_qs=[variant_obj.variant_image.all() for variant_obj in product_variant_objs]
    print("list of images",list_of_variant_image_qs)
    for index,variant_obj in enumerate(product_variant_objs):
        variant_form=ProductVariantFullForm(request.POST or None,instance=variant_obj,prefix=f"{index}_variant_form")
        variant_images=variant_obj.variant_image.all()
        prefilled_variant_forms_list.append((variant_form,variant_images,variant_obj)) #this tuple contains teh form and images queryset for that particular variant obj
    print(product_obj,product_variant_objs)
    i_pv_formset=inlineformset_factory(Product,ProductVariant,form=ProductVariantFullForm,extra=10, can_delete=True)
    formset1=i_pv_formset(instance=product_obj,queryset=ProductVariant.objects.none())
    if request.method=='POST':
        # handling new tags and badges
        post=request.POST.copy()
        tag_list=[]
        for tag_id in request.POST.getlist('tags'):
            print(tag_id)
            try:
                if ProductTag.objects.filter(id=tag_id).exists(): #if this arises any error then there exist no such tag, this error is arised because we will be getting id if already tag is exist, else we will get the name of the new tag entered and when we try to match with tag id it causes an error.
                    pass
                
                else:
                    tag_obj=ProductTag.objects.create(name=tag_id)
                    tag_id=tag_obj.id

            except:
                tag_obj=ProductTag.objects.create(name=tag_id)
                tag_id=tag_obj.id
            tag_list.append(tag_id)
            print("taglist",tag_list)

        post.setlist('tags', tag_list)

        badge_list=[]
        print("badge post",request.POST.getlist('badge'))
        for badge_id in request.POST.getlist('badge'):
            print("batch_id",badge_id)
            if badge_id!='':
                try:
                    if SpecialBadge.objects.filter(id=badge_id).exists(): #if this arises any error then there exist no such tag, this error is arised because we will be getting id if already tag is exist, else we will get the name of the new tag entered and when we try to match with tag id it causes an error.
                        pass
                    
                    else:
                        badge_obj=SpecialBadge.objects.create(name=badge_id)
                        badge_id=badge_obj.id

                except:
                    badge_obj=SpecialBadge.objects.create(name=badge_id)
                    badge_id=badge_obj.id
                badge_list.append(badge_id)
                print("badgelist",badge_list)

            post.setlist('badge', badge_list)

        category_list=[]
        for category_id in request.POST.getlist('category'):
            if category_id!='':
                try:
                    if ProductCategory.objects.filter(id=category_id).exists():
                        pass
                    else:
                        category_obj=ProductCategory.objects.create(name=category_id)
                        category_id=category_obj.id
                except:
                    category_obj=ProductCategory.objects.create(name=category_id)
                    category_id=category_obj.id
                category_list.append(category_id)
            post.setlist('category',category_list)
            
        request.POST=post
        # 
        product_form=AddProductForm(request.POST,instance=product_obj)
        formset1=i_pv_formset(request.POST,request.FILES,instance=product_obj)
        if product_form.is_valid():
            product_form.save()
            for index,zipped_items in enumerate(prefilled_variant_forms_list):
                (form,_,variant_obj) = zipped_items
                if form.is_valid():
                    form.save()
                    images=request.FILES.getlist(f'{index}_variant_form-images')
                    for image in images:
                        variant_image_obj=ProductImage.objects.create(product_variant=variant_obj,image=image)
                        # all_varaint_img_objs.append(variant_image_obj)
                        print("image saved")
                    print("prefilled form saved")
            for index,form in enumerate(formset1):
                if form.is_valid():
                    print("inise frm valid")
                    variant_obj=form.save()
                    images=request.FILES.getlist(f'product_variants-{index}-images')
                    for image in images:
                        ProductImage.objects.create(product_variant=variant_obj,image=image)
            messages.success(request,"Product Updated Successfully !!")
            return redirect('products_list')
        else:
            messages.error(request,"Failed to update!!")
            return redirect('products_list')
    # messages.success(request,"rendered")
    context={'product_form':product_form,'formset1':formset1,'list_of_variant_image_qs':list_of_variant_image_qs,'prefilled_variant_forms_list':prefilled_variant_forms_list}
    return render(request,'admin_dashboard/edit_product.html',context)

def inventory(request):
    product_variants=ProductVariant.objects.all().order_by('product')
    print(product_variants)
    context={'product_variants':product_variants}
    return render(request,'admin_dashboard/inventory.html',context)

def edit_variant(request,pk):
    variant_obj=ProductVariant.objects.get(id=pk)
    form=ProductVariantFullForm(instance=variant_obj)
    variant_images=ProductImage.objects.filter(product_variant=variant_obj)
    if request.method == 'POST':
        form=ProductVariantFullForm(request.POST,request.FILES,instance=variant_obj)
        if form.is_valid():
            form.save()
            images=request.FILES.getlist('images')
            for image in images:
                ProductImage.objects.create(product_variant=variant_obj,image=image)
            messages.success(request,"variant Updated Successfully !!")
            return redirect('inventory')
        else:
            messages.error(request,"Enter proper data!!")

    context={'form':form,'variant_images':variant_images}
    return render(request,'admin_dashboard/edit_variant.html',context)

from django.http import JsonResponse,HttpResponse
def update_stock_endpoint(request):
    print("fetch success")
    if request.method=='POST':
        variant_obj_id=request.POST.get('variant_id')
        updated_stock=request.POST.get('updated_stock')
        try:
            variant_obj=ProductVariant.objects.get(id=variant_obj_id)
            variant_obj.available_stock=int(updated_stock)
            variant_obj.save()
            return JsonResponse({'status':'success','updated_stock':variant_obj.available_stock})
        except:
            return JsonResponse({'status':'failed'})
    return JsonResponse({'status':'GET REQUEST'})


def delete_img_endpoint(request,pk):
    # print(request.data)
    try:
        image_obj=ProductImage.objects.get(id=pk)
        cover_imgs_length=len(ProductImage.objects.filter(product_variant=image_obj.product_variant))
        if cover_imgs_length>1:
            image_obj.delete()
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'unable to delete','msg':"Can't delete this, there must be atleast one image for each variant !!"})
    except:
        return JsonResponse({'status':'failed'})
        
def collections(request):
    collections=Collection.objects.all()
    context={'collections':collections,'page':'Collections'}
    return render(request,'admin_dashboard/collections.html',context)

def add_collection(request):
    form=CollectionForm(request.POST or None)
    if request.method == 'POST':
        print("post method")
        if form.is_valid():
            print("form valid")
            flag=True
            message=''
            products=form.cleaned_data['products']
            print("dict",products)
            offer=form.cleaned_data['offer']
            for product in products:
                print("product",product)
                if product.offer != None:
                    flag=False
                    message=f'{product.name} has an active offer : {product.offer}'
                    break
            if flag:
                for product in products:
                    product.offer=offer
                    product.save()
                    update_offer_price(product,product.offer)
                    
                form.save()
                messages.success(request,"New Collections Added !!")
            
                return redirect('collections')
            else:
                messages.warning(request,f"{message}")

        else:
            messages.error(request,"Something Went Wrong")
    context={'form_title':'New Collection','form':form}
    return render(request,'admin_dashboard/add_collection.html',context)

def edit_collection(request,pk):
    collection_obj=Collection.objects.get(id=pk)
    form=CollectionForm(request.POST or None,instance=collection_obj)
    
    if request.method == 'POST':
        if form.is_valid():
            print("form valid")
            flag=True
            message=''
            products=form.cleaned_data['products']
            old_products=collection_obj.products.all()
            offer=form.cleaned_data['offer']
            
            print("products-seom",set(products)-set(old_products))
            newly_added_products=list(set(products)-set(old_products))
            print("dict",products)
            for product in newly_added_products:
                # print("product",type(product),product,product.offer)
                product=Product.objects.get(id=product.id) #here we are doing this because,in the previous for loop we have updated the product by removing the offers,but the products list that we fetched earlier has old data in it, so for getting the updated product we are ding this
                if product.offer != None:
                    flag=False
                    message=f'{product.name} has an active offer : {product.offer}'
                    break
            if flag:
                for product in old_products:
                    product.offer=None
                    product.save()
                    update_offer_price(product,product.offer)
                    print("product.offer",product,product.offer)
                for product in products:
                    product.offer=offer
                    product.save()
                    update_offer_price(product,product.offer)

                form.save()
                messages.success(request,"Collection Updated Successfully !!")            
                return redirect('collections')
            else:
                messages.warning(request,f"{message}")
            # form.save()
            # 
            # return redirect('collections')
        else:
            messages.error(request,"Something Went Wrong!!")
    context={'form_title':'Edit Collection','form':form}
    return render(request,'admin_dashboard/add_collection.html',context)


def delete_collection(request,pk):
    collection_obj=Collection.objects.get(id=pk)
    products=collection_obj.products.all()
    for product in products:
        product.offer=None
        product.save()
        update_offer_price(product,product.offer)
    collection_obj.delete()
    messages.success(request,"Collection Deleted Successfully !!")
    return redirect('collections')
    
def view_collection_products_endpoint(request,pk):
    collection_obj=Collection.objects.get(id=pk)
    collection_products=collection_obj.products.all()
    products_list=[]
    for index,product in enumerate(collection_products):
        product_dict={}
        product_dict['s_no']=index+1
        product_dict['product_name']=product.name
        product_dict['product_id']=product.id
        product_dict['image_url']=product.product_variants.first().variant_image.first().image.url
        print(product_dict)
        products_list.append(product_dict)

    context={'collection_title':collection_obj.name,'product_list':products_list,'status':'success'}
    return JsonResponse(context)

def remove_product_from_collection(request,c_id,p_id):
    try:
        collection_obj=Collection.objects.get(id=c_id)
        products_obj=Product.objects.get(id=p_id)
        collection_obj.products.remove(products_obj)
        count=collection_obj.products.count()
        return JsonResponse({'status':'success','count':count})
    except:
        return JsonResponse({'status':'failed'})


def offers(request):

    offers=Offer.objects.all()
    context={'page':'Offers','offers':offers}
    
    return render(request,'admin_dashboard/offers.html',context)

def add_offer(request):
    nxt = request.GET.get("next", None)

    form=OfferForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request,'Offer added Successfully !!')
            if nxt is not None:
                return redirect(nxt)
            return redirect('offers')
        else:
            messages.error(request,"Something went wrong !!")
    context={'form':form,'form_title':'New Offer'}
    return render(request,'admin_dashboard/offer_form.html',context)

def edit_offer(request,pk):
    offer_obj=Offer.objects.get(id=pk)
    form=OfferForm(request.POST or None,instance=offer_obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request,'Offer updated Successfully !!')
            return redirect('offers')
        else:
            messages.error(request,"Something went wrong !!")
    context={'form':form,'form_title':'Edit Offer'}
    return render(request,'admin_dashboard/offer_form.html',context)

def delete_offer(request,pk):
    offer_obj=Offer.objects.get(id=pk)
    offer_obj.delete()
    messages.success(request,'Offer deleted successfully!!')
    return redirect('offers')








# from barcode import EAN13
import barcode
  
# import ImageWriter to generate an image file
from barcode.writer import ImageWriter
from teqta import settings

def check(request):
    number = 'NAW00042L'
    
    # Now, let's create an object of EAN13 class and 
    # pass the number with the ImageWriter() as the 
    # writer
    EAN = barcode.get_barcode_class('code128')
    print(EAN)
    my_code = EAN(number, writer=ImageWriter())
    
    # Our barcode is ready. Let's save it.
    img_name = f'form_id_dummy.png'
    my_code.save(settings.MEDIA_ROOT + '/product_bar_code/' + img_name)
    # my_code.save("new_code1")
    return HttpResponse("hello")
