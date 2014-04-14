# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from ab_site.forms import ContactInfoAdminForm, CountryAdminForm
from ab_site.models import ContactInfo, Employee, Country
from models import Image, Slider, Customer


def make_supported(modeladmin, request, queryset):
    queryset.update(is_supported=True)
make_supported.short_description = 'Mark selected countries as supported'


def make_unsupported(modeladmin, request, queryset):
    queryset.update(is_supported=False)
make_unsupported.short_description = 'Mark selected countries as unsupported'


class ImageAdmin(admin.ModelAdmin):
    list_display = ['verbose_name', 'url', 'view']


class ContactInfoAdmin(admin.ModelAdmin):
    form = ContactInfoAdminForm
    #exclude = ['site']


class CustomerAdmin(admin.ModelAdmin):
    exclude = ['email_hash']


class CountryAdmin(admin.ModelAdmin):
    form = CountryAdminForm
    list_display = ['code', 'name', 'is_supported']
    actions = [make_supported, make_unsupported]


class UserProfileInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'Employee profile'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(Slider)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Country, CountryAdmin)