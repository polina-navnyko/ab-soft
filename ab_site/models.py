# -*- coding: utf-8 -*-
import hashlib
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models


class Image(models.Model):
    verbose_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')

    def view(self):
        return u'<img src="%s" />' % self.image.url
    view.short_description = 'Image'
    view.allow_tags = True

    def url(self):
        return u'<a href="%s">url<a/>' % self.image.url
    url.short_description = 'Url'
    url.allow_tags = True

    def __unicode__(self):
        return self.verbose_name


class Slider(models.Model):
    image = models.ForeignKey(Image)

    class Meta:
        verbose_name_plural = 'Slider'
        verbose_name = 'Slide image'

    def __unicode__(self):
        return self.image.verbose_name


class ContactInfo(models.Model):
    #dirty singleton realisation
    site = models.OneToOneField(Site)
    body = models.TextField(verbose_name='Info')

    class Meta:
        verbose_name_plural = "Contact Info"

    def __unicode__(self):
        return u'Contact Info'


class Employee(models.Model):
    user = models.OneToOneField(User)
    position = models.CharField(max_length=255, verbose_name="Position of employee")


class Customer(models.Model):
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    country = models.ForeignKey('Country')
    email = models.EmailField(unique=True)
    email_hash = models.CharField(max_length=64, db_index=True)
    phone = models.CharField(max_length=50)
    # is_subscribed = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.email_hash = hashlib.sha256(self.email).hexdigest()
        super(Customer, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.email


class Country(models.Model):
    code = models.CharField(max_length=2, verbose_name='Country code',
                            help_text='See http://en.wikipedia.org/wiki/ISO_3166-1')
    name = models.CharField(max_length=100)
    is_supported = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Supported countries"

    def __unicode__(self):
        return self.name