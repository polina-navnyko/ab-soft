# -*- coding: utf-8 -*-
from django import forms
from tinymce.widgets import TinyMCE
from ab_site.models import Country, ContactInfo


class ContactInfoAdminForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 100, 'rows': 40}))

    class Meta:
        model = ContactInfo


class CountryAdminForm(forms.ModelForm):

    class Meta:
        model = Country

    def clean_code(self):
        return self.cleaned_data["code"].upper()