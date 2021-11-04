from django.contrib import admin
from .models import *

@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    search_filds = ('id', 'name')

@admin.register(Order)

class OrderAdmin(admin.ModelAdmin):
    search_filds = ('id',)

@admin.register(OrderDetail)

class OrderDetailAdmin(admin.ModelAdmin):
    search_filds = ('product__name',)
