'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.db import models

# Create your models here.


class Category(models.Model):
    '''Category model init with fiels'''
    name = models.CharField(max_length=200, unique=True,
                            default='DEFAULT VALUE')

    def __str__(self):
        return str(self.name)


class Contact(models.Model):
    '''Contact model init with fiels'''
    email = models.EmailField(max_length=100)
    name = models.CharField(max_length=200)


class Product(models.Model):
    '''Product model init with fiels'''
    name = models.CharField(max_length=400, unique=False)
    brands = models.CharField(max_length=400)
    nutriscore_grade = models.CharField(max_length=10, null=True)
    url = models.URLField()
    image = models.URLField()
    stores = models.CharField(max_length=400, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 null=True, default=None)

    def __str__(self):
        return str(self.name)


class Favorite(models.Model):
    '''Favorite model init with fiels'''
    product = models.ForeignKey(Product,
                                on_delete=models.PROTECT,
                                related_name='product')
    substitute = models.ForeignKey(Product,
                                   on_delete=models.PROTECT,
                                   related_name='substitute')
    username = models.CharField(max_length=100)
