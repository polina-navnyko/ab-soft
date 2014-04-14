from django.contrib import admin
from ab_payment.models import Transaction, Tax, InformationMessage, BoughtItem


class BoughtItemInline(admin.TabularInline):
    model = BoughtItem
    max_num = 0
    extra = 0
    can_delete = False
    readonly_fields = ['license', 'quantity']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['ref_id', 'amount', 'created', 'modified', 'status']
    fields = ['trans_id', 'ref_id', 'amount', 'applied_taxes', 'bounded_customer', 'status', 'notes']
    readonly_fields = ['trans_id', 'ref_id', 'notes']
    inlines = [BoughtItemInline]

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Tax)
admin.site.register(InformationMessage)