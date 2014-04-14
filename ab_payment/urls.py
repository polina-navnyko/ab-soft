# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from ab_payment.views import add_item_to_cart, contact_info, delete_item_from_cart, checkout_details, \
    checkout_result, CartView


urlpatterns = patterns('',
    url(r'^cart/$', CartView.as_view(), name='page_cart'),
    url(r'^checkout/$', contact_info, name='page_contact_info'),
    #TODO make regex safe
    url(r'^checkout/([\w+]{10})$', checkout_details, name='page_checkout_details'),
    url(r'^result/$', checkout_result, name='page_checkout_result'),

)
