# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Document


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


