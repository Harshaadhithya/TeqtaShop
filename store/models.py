from django.db import models
from users.models import Profile
from inventory.models import *
import uuid

# Create your models here.

class Order(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.UUIDField(default=uuid.uuid4,unique=True,editable=False,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_qty_total(self):
        orderitems = self.orderitem_set.all()
        # total = sum([item.quantity for item in orderitems])
        total = len(orderitems)
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.current_price * self.quantity
        return total


class ShippingAddress(models.Model):
    state_choices=(
        ('admin','admin'),
        ('customer','customer')
    )
    customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200,null=True)
    mobile=models.PositiveBigIntegerField(null=True)
    address_line_1 = models.CharField(max_length=200, null=False, blank=False)
    address_line_2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=False, blank=False)
    state = models.CharField(choices=state_choices,max_length=200, null=False, blank=False)
    zipcode = models.CharField(max_length=200, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address_line_1
