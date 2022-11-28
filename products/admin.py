# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Product, Order, OrderItem, InsuranceClaim


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'image_url')
    raw_id_fields = ('pharmacies',)
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'status',
        'pharmacy',
        'buyer',
        'price',
        'invoice',
        'prescription',
        'razorpay_payment_id',
    )
    list_filter = ('pharmacy', 'buyer', 'invoice', 'prescription')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'order')
    list_filter = ('product', 'order')


@admin.register(InsuranceClaim)
class InsuranceClaimAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'order', 'provider')
    list_filter = ('order', 'provider')
