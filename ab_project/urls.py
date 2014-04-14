from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^', include('ab_site.urls')),
    url(r'^news/', include('ab_news.urls')),
    url(r'^products/', include('ab_products.urls')),
    #TODO rename url
    url(r'^payment/', include('ab_payment.urls')),
    url(r'^admin/$', RedirectView.as_view(url='/', permanent=True)),
    url(r'^manage/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
)

if not settings.PRODUCTION:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)