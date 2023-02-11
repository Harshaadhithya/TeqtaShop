from distutils.command.upload import upload
from email.policy import default
from enum import unique
from pyexpat import model
from random import choices
from django.db import models
from users.models import Profile
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.

class Product(models.Model):
    status_choices = (
        ('Active', 'Active'),
        ('Draft', 'Draft')
    )
    name = models.CharField(max_length=255, unique=True)
    # url_name=models.CharField(max_length=255,unique=True,blank=True)
    description = RichTextUploadingField(null=True)
    status = models.CharField(max_length=100, choices=status_choices, default='Active')
    general_price = models.DecimalField(max_digits=10, decimal_places=2)
    # vendor=models.CharField(max_length=200,null=True,blank=True)
    total_reviews = models.PositiveIntegerField(default=0, null=True, blank=True)
    avg_rating = models.DecimalField(default=0, max_digits=2, decimal_places=1)
    tags = models.ManyToManyField('ProductTag', blank=True)
    category=models.ManyToManyField('ProductCategory',blank=True)
    offer = models.ForeignKey('Offer', null=True, blank=True, on_delete=models.SET_NULL)
    badge = models.ForeignKey("SpecialBadge", on_delete=models.SET_NULL, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created']

    @property
    def apply_offer_price(self):
        if self.offer != None or self.offer != '':
            product_variants = self.product_variants.all()
            for product_variant in product_variants:
                product_variant.current_price = product_variant.current_price - (
                            product_variant.current_price * (self.offer.percentage / 100))
                product_variant.save()

    @property
    def revert_offer_price(self):
        product_variants = self.product_variants.all()
        for product_variant in product_variants:
            product_variant.current_price = product_variant.original_price
            product_variant.save()

    def __str__(self):
        return self.name


class VariantType(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Variant(models.Model):
    variant_type = models.ForeignKey(VariantType, on_delete=models.CASCADE)
    variant_name = models.CharField(max_length=200)
    value = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.variant_type}-{self.variant_name}'

class ProductCategory(models.Model):
    name=models.CharField(max_length=200,unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    varaint_type_choices = (
        ('color', 'color'),
        ('other', 'other')
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variants', null=True,
                                blank=True)
    description = RichTextUploadingField(null=True, blank=True)
    table_content = RichTextUploadingField(null=True, blank=True)
    # colors,sizes,etc...
    variant_type = models.CharField(max_length=100, null=True, choices=varaint_type_choices, default='other')
    variant_name = models.CharField(max_length=200, null=True, blank=True)
    value = models.CharField(max_length=100, null=True, blank=True)
    # 
    compatible_with = models.ManyToManyField('Compatibilty')
    total_stock = models.PositiveIntegerField(default=0)
    available_stock = models.PositiveIntegerField(default=0)
    total_sales = models.PositiveIntegerField(default=0)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    bar_code = models.ImageField(null=True, blank=True, upload_to='product_bar_code/')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['product', 'variant_name']]
        ordering = ['variant_type', 'value']

    # def __str__(self):

    #     return f'{self.product.name}-{self.variant_type}-{self.variant_name}'



class ProductImage(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='variant_image')
    image = models.ImageField(null=False, blank=False, upload_to='product_images/')

    def __str__(self):
        if self.product_variant != None:
            return f"{self.product_variant.product.name}-{self.product_variant.variant_name}"
        else:
            return self.product_variant.product.name


class Compatibilty(models.Model):
    name=models.CharField(max_length=200,unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Offer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    percentage = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.percentage}%"


class Collection(models.Model):
    status_choices = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    )
    name = models.CharField(max_length=200, unique=True)
    products = models.ManyToManyField("Product", blank=True)
    offer = models.ForeignKey(Offer, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, choices=status_choices, default='Active', blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.PositiveIntegerField(default=1, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['owner', 'product']]

    def __str__(self):
        return f"{self.product.name}-{self.owner.email}"


class ProductTag(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SpecialBadge(models.Model):
    name = models.CharField(max_length=100,null=False)

    def __str__(self):
        return self.name


def productsList():
    return Product.objects.all()

class Coupon(models.Model):
    type_choices=(
        ('percentage','percentage'),
        ('cashback','cashback') #price reduction
    )
    status_choices=(
        ('Active','Active'),
        ('Inactive','Inactive')
    )
    

    name = models.CharField(max_length=200,unique=True)
    coupon_type = models.CharField(max_length=200,choices=type_choices,default='percentage')
    value = models.PositiveBigIntegerField()
    applicable_products = models.ManyToManyField('Product',blank=True,default=productsList)
    min_checkout_price = models.PositiveBigIntegerField(default=1)
    status = models.CharField(max_length=100,default='Active',choices=status_choices)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering=['status','-created']





