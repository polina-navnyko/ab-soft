# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from ab_products.models import SoftwareProduct, License
from ab_site.models import Customer

TRANSACTION_PREPARING = 0
TRANSACTION_PENDING = 1
TRANSACTION_SUCCESS = 2
TRANSACTION_FAILED = 3


class Transaction(models.Model):
    TRANSACTION_STATUS_CHOICES = (
        (TRANSACTION_PREPARING, 'Preparing'),  # default status
        (TRANSACTION_PENDING, 'Pending'),
        (TRANSACTION_SUCCESS, 'Success'),
        (TRANSACTION_FAILED, 'Failed'),
    )
    prefix = 'AB'
    ref_id_pattern = '%(prefix)s%(number)08d'
    trans_id = models.BigIntegerField(null=True, blank=True)
    ref_id = models.CharField(max_length=50, null=True, blank=True)
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    applied_taxes = models.ManyToManyField('Tax', null=True, blank=True)
    bounded_customer = models.ForeignKey(Customer, null=True, blank=True)
    status = models.IntegerField(choices=TRANSACTION_STATUS_CHOICES, default=TRANSACTION_PREPARING)
    notes = models.CharField(max_length=20, null=True, blank=True)

    def __unicode__(self):
        return self.ref_id


class Tax(models.Model):
    name = models.CharField(max_length=255)
    rate = models.FloatField()
    apply = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Taxes'

    def to_percent(self):
        return self.rate * 100

    def __unicode__(self):
        return self.name


class BoughtItem(models.Model):
    license = models.ForeignKey(License)
    quantity = models.IntegerField()
    transaction = models.ForeignKey(Transaction)


class InformationMessage(models.Model):
    text = models.TextField()
    show = models.BooleanField(default=True)

    def __unicode__(self):
        return self.text


def create_ref_id(sender, instance, created, *args, **kwargs):
    if created:
        instance.ref_id = instance.ref_id_pattern % dict(prefix=instance.prefix, number=instance.id)
        instance.save(force_update=True)


post_save.connect(create_ref_id, sender=Transaction)