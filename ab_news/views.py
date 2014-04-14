# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from ab_news.models import Article
from ab_site.models import Customer


def show_news(request):
    context = {}
    news = Article.objects.all().order_by('-created')
    context['news'] = news
    return render_to_response('news.html', context)


def unsubscribe(request, email_hash):
    email = get_object_or_404(Customer, email_hash=email_hash)
    email.is_subscribed = False
    email.save()
    return HttpResponse('unsubscribed : %s' % email.email)


