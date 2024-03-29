from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm
from inventory.models import *
from django import forms


class AddProductForm(ModelForm):
    class Meta:
        model=Product
        fields='__all__'
        exclude=['avg_rating','total_reviews']

    def __init__(self,*args,**kwargs):
        super(AddProductForm,self).__init__(*args,**kwargs)
        self.fields['name'].widget.attrs.update({'class':'form-control'})
        self.fields['status'].widget.attrs.update({'class':'form-control selectric'})
        self.fields['description'].widget.attrs.update({'class':'form-control'})
        self.fields['description'].required=True
        self.fields['general_price'].widget.attrs.update({'class':'form-control currency'})
        self.fields['badge'].widget.attrs.update({'class':'select2-tags form-control'})
        self.fields['tags'].widget.attrs.update({'class':'select2-tags form-control'})
        self.fields['category'].widget.attrs.update({'class':'select2-tags form-control'})

        # self.fields['tags'].widget.attrs.update({'class':'select-item form-control'})

class ProductVariantForm(ModelForm):
    
    class Meta:
        model=ProductVariant
        fields='__all__'
        exclude=['product']

    def __init__(self,*args,**kwargs):
            super(ProductVariantForm,self).__init__(*args,**kwargs)
            self.fields['total_stock'].widget.attrs.update({'class':'form-control'})
            self.fields['variant'].widget.attrs.update({'class':'form-control selectric'})
            self.fields['available_stock'].widget.attrs.update({'class':'form-control'})
            self.fields['total_sales'].widget.attrs.update({'class':'form-control'})
            self.fields['original_price'].widget.attrs.update({'class':'form-control currency'})
            self.fields['current_price'].widget.attrs.update({'class':'form-control currency'})
            self.fields['compatible_with'].widget.attrs.update({'class':'select2-tags form-control'})
            # self.fields['tags'].widget.attrs.update({'class':'select2-tags form-control'})
    




class ProductVariantFullForm(ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)

    class Meta:
        model=ProductVariant
        fields=['description','table_content','variant_type','variant_name','value','compatible_with','total_stock','available_stock','original_price','current_price']
        # exclude=['product']

    
        
    def __init__(self,*args,**kwargs):
            super(ProductVariantFullForm,self).__init__(*args,**kwargs)
            self.empty_permitted = False
            self.fields['total_stock'].widget.attrs.update({'class':'form-control'})
            self.fields['variant_type'].widget.attrs.update({'class':'form-control select2-tags'})
            self.fields['variant_name'].widget.attrs.update({'class':'form-control'})
            self.fields['value'].widget.attrs.update({'class':'form-control'})
            self.fields['available_stock'].widget.attrs.update({'class':'form-control'})
            # self.fields['total_sales'].widget.attrs.update({'class':'form-control'})
            self.fields['original_price'].widget.attrs.update({'class':'form-control currency'})
            self.fields['current_price'].widget.attrs.update({'class':'form-control currency'})
            self.fields['compatible_with'].widget.attrs.update({'class':'select2-tags form-control'})

           



class CollectionForm(ModelForm):
    class Meta:
        model=Collection
        fields='__all__'

    def __init__(self,*args,**kwargs):
            super(CollectionForm,self).__init__(*args,**kwargs)
            self.fields['name'].widget.attrs.update({'class':'form-control'})
            self.fields['offer'].widget.attrs.update({'class':'form-control select2'})
            self.fields['products'].widget.attrs.update({'class':'form-control select2'})
            self.fields['status'].widget.attrs.update({'class':'form-control'})


class OfferForm(ModelForm):
    class Meta:
        model=Offer
        fields='__all__'

    def __init__(self,*args,**kwargs):
            super(OfferForm,self).__init__(*args,**kwargs)
            self.fields['name'].widget.attrs.update({'class':'form-control'})
            self.fields['percentage'].widget.attrs.update({'class':'form-control'})

class CouponForm(ModelForm):
    class Meta:
        model=Coupon
        fields='__all__'

    def __init__(self,*args,**kwargs):
        super(CouponForm,self).__init__(*args,**kwargs)
        self.fields['name'].widget.attrs.update({'class':'form-control'})
        self.fields['coupon_type'].widget.attrs.update({'class':'form-control'})
        self.fields['value'].widget.attrs.update({'class':'form-control'})
        self.fields['applicable_products'].widget.attrs.update({'class':'form-control select2'})
        self.fields['min_checkout_price'].widget.attrs.update({'class':'form-control'})
        self.fields['status'].widget.attrs.update({'class':'form-control selectric'})