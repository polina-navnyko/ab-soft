# -*- coding: utf-8 -*-
from django.contrib import admin
from models import SoftwareProduct, Comment, InstallPackage, Camera, CameraResolution, CameraSeries, CameraInterfaceType, License
from forms import ProductAdminForm


class InstallPackageInline(admin.StackedInline):
    model = InstallPackage


class CommentInline(admin.TabularInline):
    model = Comment


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['name']
    ordering = ['name']
    fieldsets = [
        (None, {'fields': ['name', 'thumbnail', 'logo', 'short_description', 'full_description', 'license']}),
    ]
    inlines = [InstallPackageInline, CommentInline]


class CameraInline(admin.TabularInline):
    model = Camera


class CameraAdmin(admin.ModelAdmin):
    list_display = ['code', 'series', 'type', 'sensor',
                    'resolution', 'FPS', 'bits', 'price']
    list_filter = ['interface_type', 'color_type', 'series', 'resolution']


class CameraSeriesAdmin(admin.ModelAdmin):
    inlines = (CameraInline,)

admin.site.register(SoftwareProduct, ProductAdmin)
admin.site.register(InstallPackage)
admin.site.register(License)
admin.site.register(Camera, CameraAdmin)
admin.site.register(CameraResolution)
admin.site.register(CameraSeries, CameraSeriesAdmin)
admin.site.register(CameraInterfaceType)