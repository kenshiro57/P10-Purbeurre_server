'''!/usr/bin/python3
   -*- coding: Utf-8 -'''

import requests

from ..models import Product


def product_search(search_request):
    ''' Return searched product model query '''
    product = Product.objects.filter(
        name__icontains=search_request)
    return product


def substitute_search(search_request):
    ''' Return all substitute of the selected product as model query '''
    product = Product.objects.filter(
        name__icontains=search_request)
    my_product = product[0]
    my_product_nutriscore = my_product.nutriscore_grade
    if my_product_nutriscore == 'e':
        list_score = ["d", "c", "b", "a"]
        substitutes_search = Product.objects.filter(
            category_id=my_product.category_id).filter(
            nutriscore_grade__in=list_score).exclude(
            id=my_product.id)
    elif my_product_nutriscore == 'd':
        list_score = ["c", "b", "a"]
        substitutes_search = Product.objects.filter(
            nutriscore_grade__in=list_score).filter(
            category_id=my_product.category_id).exclude(
            id=my_product.id)
    elif my_product_nutriscore == 'c':
        list_score = ["c", "b", "a"]
        substitutes_search = Product.objects.filter(
            nutriscore_grade__in=list_score).filter(
            category_id=my_product.category_id).exclude(
            id=my_product.id)
    elif my_product_nutriscore == 'b':
        list_score = ["b", "a"]
        substitutes_search = Product.objects.filter(
            nutriscore_grade__in=list_score).filter(
            category_id=my_product.category_id).exclude(
            id=my_product.id)
    else:
        list_score = ["a"]
        substitutes_search = Product.objects.filter(
            nutriscore_grade__in=list_score).filter(
            category_id=my_product.category_id).exclude(
            id=my_product.id)
    return substitutes_search

def get_data_opf(name):
    url = 'https://fr.openfoodfacts.org/cgi/search.pl?'
    category_name = 'pizza'
    payload = {"search_terms": name,
               "json": 1,
               "charset": "windows-1252",
               "action": "process",
               "lang": "fr",
               "page_size": "100",
               "page": "1"
               }
    response = requests.get(url, param=payload,)
    return response.json()
