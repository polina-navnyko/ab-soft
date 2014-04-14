# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'^$', show_news, name='page_news'),
    url(r'^unsubscribe/(?P<email_hash>[a-f0-9]{64})$', unsubscribe, name='action_unsubscribe')
)