# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Organization, PersonalUser, CustomUserProxy

admin.site.register(CustomUser, UserAdmin)


@admin.register(CustomUserProxy)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_active',)
    readonly_fields = ('id', 'email')
    fields = ('id', 'email', 'is_active')
    search_fields = ('email',)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'category',
        'description',
        'images',
        'location',
        'custom_user',
        'licenses',
        'permits',
    )
    list_filter = ('custom_user',)


@admin.register(PersonalUser)
class PersonalUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'category',
        'address',
        'date_of_birth',
        'proof_of_identity',
        'proof_of_address',
        'health_license',
        'custom_user',
        'organization',
    )
    list_filter = ('date_of_birth', 'custom_user', 'organization')
