# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Document, DocumentVerificationRequest


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'document',
        'uploaded_at',
        'custom_user',
        'sha_256',
    )
    list_filter = ('uploaded_at', 'custom_user')
    raw_id_fields = ('shared_with',)


@admin.register(DocumentVerificationRequest)
class DocumentVerificationRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'document',
        'requested_by',
        'created_at',
        'requested_to',
        'transaction_hash',
    )
    list_filter = ('document', 'requested_by', 'created_at', 'requested_to')
    date_hierarchy = 'created_at'
