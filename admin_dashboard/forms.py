from pyexpat import model
from django.forms import ModelForm
from inventory.models import *

class AddProductForm(ModelForm):
    class Meta:
        model=Product
        fields='__all__'