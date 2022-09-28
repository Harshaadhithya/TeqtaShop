from email.policy import default
from enum import unique
from pyexpat import model
from random import choices
from django.db import models
from users.models import Profile

# Create your models here.

class Product(models.Model):
    status_choices=(
        ('Active','Active'),
        ('Draft','Draft')
    )
    name=models.CharField(max_length=255,unique=True)
    description=models.TextField(null=True)
    status=models.CharField(max_length=100,choices=status_choices)
    general_price=models.DecimalField(max_digits=10,decimal_places=2)
    vendor=models.CharField(max_length=200,null=True,blank=True)
    total_reviews=models.PositiveIntegerField(default=0,null=True,blank=True)
    avg_rating=models.DecimalField(default=0,max_digits=2,decimal_places=1)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class VariantType(models.Model):
    name=models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.name

class Variant(models.Model):
    variant_type=models.ForeignKey(VariantType,on_delete=models.CASCADE)
    variant_name=models.CharField(max_length=200)
    value=models.CharField(max_length=100)
    created=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.variant_type}-{self.variant_name}'

class ProductVariant(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_variants')
    variant=models.ForeignKey(Variant,on_delete=models.SET_NULL,null=True,blank=True)
    total_stock=models.PositiveIntegerField(default=0,null=True)
    available_stock=models.PositiveIntegerField(default=0,null=True)
    total_sales=models.PositiveIntegerField(default=0,null=True)
    original_price=models.DecimalField(max_digits=10, decimal_places=2)
    current_price=models.DecimalField(max_digits=10, decimal_places=2)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=[['product','variant']]

    def __str__(self):
        if self.variant!=None:
            return f'{self.product.name}-{self.variant.variant_name}'
        else:
            return self.product.name

class ProductImage(models.Model):
    product_variant=models.ForeignKey(ProductVariant,on_delete=models.CASCADE,related_name='variant_image')
    image=models.ImageField(null=False,blank=False,upload_to='product_images/')

    def __str__(self):
        if self.product_variant.variant!=None:
            return f"{self.product_variant.product.name}-{self.product_variant.variant}"
        else:
            return self.product_variant.product.name


class Collection(models.Model):
    name=models.CharField(max_length=200)
    products=models.ManyToManyField("Product",blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    owner=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    body=models.TextField(null=True,blank=True)
    value=models.PositiveIntegerField(default=1,null=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=[['owner','product']]

    def __str__(self):
        return f"{self.product.name}-{self.owner.email}"

