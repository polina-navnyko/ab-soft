# Create your views here.
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import TemplateView

from ab_news.models import Article
from ab_site.models import Slider, ContactInfo


def home(request):
    context = {}
    news = Article.objects.all().order_by('-created')[:5]
    slider_images = Slider.objects.all()
    context['latest_news'] = news
    context['slides'] = slider_images
    return render_to_response('index.html', context)


class ServicesView(TemplateView):
    template_name = 'index.html'


class PortfolioView(TemplateView):
    template_name = 'index.html'


class CustomersView(TemplateView):
    template_name = 'index.html'


class PartnersView(TemplateView):
    template_name = 'index.html'


class SupportView(TemplateView):
    template_name = 'index.html'


def contacts(request):
    context = {'contact_info': get_object_or_404(ContactInfo, site=Site.objects.get_current())}
    return render_to_response('contacts.html', context)