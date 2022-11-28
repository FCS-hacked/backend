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
        'signed_by_professional',
        'signed_by_hospital',
        'signed_by_pharmacy',
        'signed_by_insurance_firm',
    )
    list_filter = (
        'uploaded_at',
        'custom_user',
        'signed_by_professional',
        'signed_by_hospital',
        'signed_by_pharmacy',
        'signed_by_insurance_firm',
    )
    raw_id_fields = ('shared_with',)
