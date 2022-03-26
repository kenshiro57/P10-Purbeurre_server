'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


import requests

from django.core.management.base import BaseCommand
from mes_aliments.models import Product


class Command(BaseCommand):
    args = '<team_id>'
    help = 'Affiche la liste des backlogs'

    def handle(self, *args, **options):
        self.url = "https://fr.openfoodfacts.org/cgi/search.pl?"
        for product in Product.objects.all():
            self.payload = {"search_terms": product.name,
                            "search_simple": 1,
                            "json": 1,
                            "charset": "utf-8",
                            "action": "process",
                            "lang": "fr"}
            self.json_request = requests.get(self.url,
                                             params=self.payload,)
            self.json_data = self.json_request.json()
            for i in range(len(self.json_data['products'])):
                self.product_data = self.json_data['products'][i]
                if product.url is not None and self.product_data.get(
                        'url') == product.url:
                    if self.product_data.get('name') is not None:
                        product.name = self.product_data.get('name')
                    if self.product_data.get('brands') is not None:
                        product.brands = self.product_data.get('brands')
                    if self.product_data.get('nutriscore_grade') is not None:
                        product.nutriscore_grade = self.product_data.get(
                            'nutriscore_grade')
                    if self.product_data.get('image_url') is not None:
                        product.image = self.product_data.get('image_url')
                    if self.product_data.get('stores') is not None:
                        product.stores = self.product_data.get('stores')
                    product.save()


