# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Product, Order, OrderEntry


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'image_url')
    raw_id_fields = ('pharmacies',)
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'pharmacy', 'buyer', 'price')
    list_filter = ('pharmacy', 'buyer')


@admin.register(OrderEntry)
class OrderEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'order')
    list_filter = ('product', 'order')
