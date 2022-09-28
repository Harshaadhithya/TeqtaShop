from enum import unique
from random import choices
from secrets import choice
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class State(models.Model):
    name=models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    name=models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    role_choices=(
        ('admin','admin'),
        ('customer','customer')
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=100,choices=role_choices,null=True,default='customer')
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    email=models.EmailField(max_length=400,unique=True,null=True)
    username=models.CharField(max_length=200)
    mobile=models.PositiveBigIntegerField(unique=True,null=True)
    address=models.TextField(null=True)
    city=models.CharField(max_length=200,null=True)
    state=models.ForeignKey(State,on_delete=models.SET_NULL,null=True)
    country=models.ForeignKey(Country,on_delete=models.SET_NULL,null=True)
    pincode=models.PositiveIntegerField(null=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email}-{self.mobile}"


