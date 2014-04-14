# -*- coding: utf-8 -*-
import json

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView

from braces.views import AjaxResponseMixin, JSONResponseMixin, CsrfExemptMixin

from ab_payment.forms import CustomerInfoForm, PaymentForm
from ab_payment.models import Transaction, Tax, TRANSACTION_PREPARING, TRANSACTION_PENDING
from ab_site.models import Customer
from ab_payment.utils import Cart


@require_POST
@csrf_exempt
def add_item_to_cart(request):
    item_code = request.POST.get('license_code', None)
    quantity = int(request.POST.get('quantity', None))
    if item_code and quantity is None:
        raise PermissionDenied
    if request.session.session_key is None:
        request.session.create()
    cart = Cart(request)
    cart.add(item_code, quantity)
    cart.save(request)
    return HttpResponse(json.dumps({'status': "ok"}), content_type="application/json")


@require_POST
@csrf_exempt
def delete_item_from_cart(request):
    item_code = request.POST.get('license_code', None)
    if item_code is None:
        raise PermissionDenied
    cart = Cart(request)
    cart.remove(item_code)
    cart.save(request)
    return HttpResponse(json.dumps({'status': "ok"}), content_type="application/json")


def contact_info(request):
    if request.method == "POST":
        try:
            customer = Customer.objects.get(email=request.POST['email'])
        except Customer.DoesNotExist:
            customer = Customer()
        form = CustomerInfoForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            request.session['customer_id'] = customer.id
            request.session.modified = True
            transaction = Transaction.objects.create()
            return HttpResponseRedirect(reverse('page_checkout_details', args=(transaction.ref_id,)))
    else:
        customer_id = request.session.get('customer_id', None)
        if customer_id is not None:
            customer = Customer.objects.get(pk=customer_id)
            form = CustomerInfoForm(instance=customer)
        else:
            form = CustomerInfoForm()
    return render_to_response('contact_info.html', {'form': form}, context_instance=RequestContext(request))


def checkout_details(request, transaction_id):
    context = {
        'cart': [],
        'summary': 0,
        'taxes': [],
        'overall': 0,
        'form': None,
    }
    transaction = get_object_or_404(Transaction, ref_id=transaction_id)
    if transaction.status == TRANSACTION_PREPARING:
        cart = Cart(request, strict=True)
        context['cart'] = cart.get_all()
        context['summary'] = cart.summary()
        taxes = Tax.objects.filter(apply=True)
        transaction.applied_taxes = taxes
        overall = context['summary']
        for tax in taxes:
            overall += context['summary'] * tax.rate
        context['overall'] += overall
        context['taxes'] = taxes
        transaction.amount = context['overall']
        transaction.status = TRANSACTION_PENDING
        transaction.save()
        form = PaymentForm(initial={'ref_id': transaction.ref_id, 'amount': transaction.amount})
        context['form'] = form
        return render_to_response('checkout_details.html', context)
    elif transaction.status == TRANSACTION_PENDING:
        form = PaymentForm(initial={'ref_id': transaction.ref_id, 'amount': transaction.amount})
        context['overall'] = transaction.amount
        context['form'] = form
        return render_to_response('checkout_details.html', context)
    return HttpResponse(transaction)


@csrf_exempt
def checkout_result(request):
    raise NotImplemented


class CartView(CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context.update({'cart': [], 'summary': 0})
        cart = Cart(self.request)
        if cart.is_empty():
            return context
        context['cart'] = cart.get_all()
        context['summary'] = cart.summary()
        return context

    def post_ajax(self, request, *args, **kwargs):
        item_code = request.POST.get('license_code', None)
        quantity = int(request.POST.get('quantity', None))
        if item_code and quantity is None:
            raise PermissionDenied
        if request.session.session_key is None:
            request.session.create()
        cart = Cart(request)
        cart.add(item_code, quantity)
        cart.save(request)
        return self.render_json_response({"status": "ok"})

    def put_ajax(self, request, *args, **kwargs):
        raise NotImplemented

    def delete_ajax(self, request, *args, **kwargs):
        cart = Cart(request)
        cart.clear()
        cart.save(request)
        return self.render_json_response({"status": "ok"})