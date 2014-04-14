# -*- coding: utf-8 -*-
from django import forms
from ab_project.settings import PAYMENT_MERCHANT_ID, PAYMENT_REDIRECT_URL, PAYMENT_REG_KEY, PAYMENT_TRANSACTION_TYPE
from ab_site.models import Country, Customer


class CustomerInfoForm(forms.ModelForm):
    country = forms.ModelChoiceField(Country.objects.filter(is_supported=True))
    #is_subscribed = forms.BooleanField(label='subscribe to our newsletter')

    class Meta:
        model = Customer
        exclude = ['email_hash']


class PaymentForm(forms.Form):
    MerchantID = forms.IntegerField(widget=forms.HiddenInput, initial=PAYMENT_MERCHANT_ID)
    RegKey = forms.CharField(widget=forms.HiddenInput, initial=PAYMENT_REG_KEY)
    RURL = forms.URLField(widget=forms.HiddenInput, initial=PAYMENT_REDIRECT_URL)
    TransType = forms.CharField(widget=forms.HiddenInput, initial=PAYMENT_TRANSACTION_TYPE)
    RefID = forms.CharField(widget=forms.HiddenInput)
    amount = forms.FloatField(widget=forms.HiddenInput)
