# -*- coding: utf-8 -*-
import json
from django.core.exceptions import PermissionDenied
from ab_products.models import License


#TODO check browser for cookie support
class Cart(object):
    def __init__(self, request, strict=False):
        self.strict = strict
        cart_json = request.session.get('cart', None)
        if cart_json is None and strict:
            raise PermissionDenied
        elif cart_json is not None:
            self.cart = json.loads(cart_json)
        else:
            self.cart = {}

    def add(self, item_code, quantity=1):
        self.cart[item_code] = self.cart.get(item_code, 0) + quantity

    def remove(self, item_code, quantity=1):
        if item_code in self.cart:
            amount = self.cart[item_code]
            if amount > quantity:
                self.cart[item_code] -= quantity
            else:
                self.cart[item_code] = 0

    def delete(self, item_code):
        del self.cart[item_code]

    def clear(self):
        self.cart = {}

    def summary(self):
        result = 0
        for license_code in self.cart.keys():
            quantity = self.cart[license_code]
            try:
                product_license = License.objects.get(code=license_code)
                result += product_license.price * quantity
            except License.DoesNotExist:
                pass
        return result

    def count(self):
        result = 0
        for license_code in self.cart.keys():
            result += self.cart[license_code]
        return result

    def save(self, request):
        request.session['cart'] = json.dumps(self.cart)
        request.session.modified = True

    def get_all(self):
        result = []
        for license_code in self.cart.keys():
            quantity = self.cart[license_code]
            try:
                product_license = License.objects.get(code=license_code)
                result.append((product_license, quantity))
            except License.DoesNotExist:
                pass
        return result

    def is_empty(self):
        return False if self.cart else True

