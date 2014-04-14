# -*- coding: utf-8 -*-
from django import forms
from tinymce.widgets import TinyMCE
from models import SoftwareProduct


class ProductAdminForm(forms.ModelForm):
    full_description = forms.CharField(widget=TinyMCE(attrs={'cols': 100, 'rows': 40}))

    class Meta:
        model = SoftwareProduct