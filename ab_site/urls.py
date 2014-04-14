# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from views import *

urlpatterns = patterns('',
    url(r'^$', home, name='page_home'),
    url(r'^services/$', ServicesView.as_view(), name='page_services'),
    url(r'^portfolio/$', PortfolioView.as_view(), name='page_portfolio'),
    url(r'^customers/$', CustomersView.as_view(), name='page_customers'),
    url(r'^partners/$', PartnersView.as_view(), name='page_partners'),
    url(r'^support/$', SupportView.as_view(), name='page_support'),
    url(r'^contacts/$', contacts, name='page_contacts'),

)
