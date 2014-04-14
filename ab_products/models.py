# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from ab_site.models import Image

CAMERA_COLOR_TYPE_CHOICES = (
    ('M', 'Monochrome'),
    ('C', 'Color'),
)


class SoftwareProduct(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField()
    thumbnail = models.ForeignKey(Image, related_name='+')
    logo = models.ForeignKey(Image, related_name='+')
    short_description = models.TextField()
    full_description = models.TextField()
    license = models.ManyToManyField("License")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SoftwareProduct, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ab_products.views.products', kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.name


class InstallPackage(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=40)
    file = models.FileField(upload_to='install')
    product = models.ForeignKey(SoftwareProduct)

    def __unicode__(self):
        return u'{name}: v{version_number}'.format(name=self.name, version_number=self.version)


class Comment(models.Model):
    text = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    product = models.ForeignKey(SoftwareProduct, related_name='comments')


class License(models.Model):
    code = models.CharField(max_length=10)
    verbose_name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()

    def __unicode__(self):
        return self.code


class CameraSeries(models.Model):
    name = models.CharField(max_length=255)
    logo = models.OneToOneField(Image)

    class Meta:
        verbose_name_plural = 'Camera series'

    def __unicode__(self):
        return u'{series_name} series'.format(series_name=self.name)


class CameraResolution(models.Model):
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    class Meta:
        ordering = ['width', 'height']
        unique_together = ['width', 'height']

    def __unicode__(self):
        return u'{width}x{height}'.format(width=self.width, height=self.height)


class CameraInterfaceType(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Camera(models.Model):
    interface_type = models.ForeignKey(CameraInterfaceType)
    color_type = models.CharField(max_length=1, choices=CAMERA_COLOR_TYPE_CHOICES)
    series = models.ForeignKey(CameraSeries)
    code = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    sensor = models.CharField(max_length=100)
    resolution = models.ForeignKey(CameraResolution)
    FPS = models.PositiveIntegerField(verbose_name='Frames Per Second')
    bits = models.PositiveIntegerField()
    price = models.IntegerField()

    def __unicode__(self):
        return self.code

    def show_price(self):
        return u'$ %s' % self.price
    show_price.short_description = 'Price'
    show_price.allow_tags = True
