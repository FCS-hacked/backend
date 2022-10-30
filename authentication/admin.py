# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import CustomUser, Organization, PersonalUser

from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser, UserAdmin)


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
