from django.forms import ModelForm
from .models import *

class ShippingForm(ModelForm):
    class Meta:
        model=ShippingAddress
        exclude=['customer','order','date_added']

    def __init__(self,*args,**kwargs):
        super(ShippingForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs.update({'class':'form-control','placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({'class':'form-control','placeholder':'Last Name'})
        self.fields['mobile'].widget.attrs.update({'class':'form-control','placeholder':'Mobile'})
        self.fields['address_line_1'].widget.attrs.update({'class':'form-control','placeholder':'Address Line 1'})
        self.fields['city'].widget.attrs.update({'class':'form-control','placeholder':'City'})
        self.fields['state'].widget.attrs.update({'class':'form-select','placeholder':'State'})
        self.fields['zipcode'].widget.attrs.update({'class':'form-control','placeholder':'Zipcode'})
        self.fields['address_line_2'].widget.attrs.update({'class':'form-control','placeholder':'Address Line 2'})

     