# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from ab_products.models import SoftwareProduct, Comment


def products(request, slug=None):
    context = {}
    if slug is None:
        context['product_list'] = SoftwareProduct.objects.all().order_by('-name')
        return render_to_response('product_list.html', context)
    #showcase
    elif slug == 'example':
        return render_to_response('product_example.html')
    else:
        context['product'] = get_object_or_404(SoftwareProduct, slug=slug)
        return render_to_response('product.html', context)


def pricing(request, slug=None):
    context = {}
    product = get_object_or_404(SoftwareProduct, slug=slug)
    context['price_list'] = product.license.all()
    context['product_name'] = product.name
    return render_to_response('pricing.html', context)