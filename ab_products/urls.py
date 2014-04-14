# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from ab_products.views import products, pricing

urlpatterns = patterns('',
    url(r'^$', products, name='page_products'),
    url(r'^(?P<slug>[\w-]+)/$', products, name='page_products'),
    url(r'^(?P<slug>[\w-]+)/pricing/$', pricing, name='page_product_pricing')
)
