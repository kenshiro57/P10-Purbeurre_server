'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


import requests
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from mock import patch

from ..models import Category, Product
from ..helper.function import substitute_search, product_search
""" Django Unittest including medthods, views and database """
""" Using Testcase library from Django Test """


class OpenFoodFactsAPITestCase(TestCase):
    ''' Product data insertion in database '''
    def setUp(self):
        ''' Init the test with multiple variables'''
        self.url = 'https://fr.openfoodfacts.org/cgi/search.pl?'
        self.category_name = 'pizza'
        self.payload = {"search_terms": self.category_name,
                                "json": 1,
                                "charset": "windows-1252",
                                "action": "process",
                                "lang": "fr",
                                "page_size": "100",
                                "page": "1"
                                }

    @patch('mes_aliments.data.requests.get')
    def test_get_data_openfoodfacts(self):
        '''  '''
        self.return_value.ok = True
        response = requests.get(self.url)
        self.assertTrue(response)



class ModelsTestCase(TestCase):
    '''Models test class'''
    def setUp(self):
        '''Init the test with creation of one category and one product'''
        self.category_name = ['pizza', 'boisson']
        self.pizza_name = ['pizza1', 'pizza2', 'pizza3', 'pizza4', 'pizza5',
                           'pizza6']
        self.pizza_nutriscore = ['a', 'c', 'b', 'd', 'e', 'a']
        for name in self.category_name:
            self.category = Category.objects.create(name=name)
        for name, nutriscore in zip(self.pizza_name, self.pizza_nutriscore):
            self.pizza = Product.objects.create(
                name=name, brands='marque', nutriscore_grade=nutriscore,
                url='url', image='image', stores='magasin')
            self.pizza.category = Category.objects.get(name='pizza')
            self.pizza.save()
        self.boisson1 = Product.objects.create(
            name='boisson1', brands='marque', nutriscore_grade='b',
            url='url', image='image', stores='magasin')
        self.boisson1 = Category.objects.get(name='boisson')
        self.boisson1.save()

    def test_product_search(self):
        '''Test the product_search method if returns the correct value'''
        self.my_product = product_search('pizza1')[0]
        self.assertEqual(self.my_product.__str__(), 'pizza1')
        self.pizza_category = Category.objects.get(name='pizza')
        self.assertEqual(self.pizza_category.__str__(), 'pizza')

    def test_substitute_search(self):
        '''Test the substitute_search method if returns the correct values'''
        self.assertEqual(substitute_search('pizza3')[0].name, 'pizza6')
        self.assertEqual([substitute_search('pizza5')[0].name,
                          substitute_search('pizza5')[1].name,
                          substitute_search('pizza5')[2].name,
                          substitute_search('pizza5')[3].name,
                          substitute_search('pizza5')[4].name],
                         ['pizza1', 'pizza2', 'pizza3', 'pizza4', 'pizza6'])
        self.assertEqual([substitute_search('pizza4')[0].name,
                          substitute_search('pizza4')[1].name,
                          substitute_search('pizza4')[2].name,
                          substitute_search('pizza4')[3].name],
                         ['pizza1', 'pizza2', 'pizza3', 'pizza6'])
        self.assertEqual([substitute_search('pizza2')[0].name,
                          substitute_search('pizza2')[1].name,
                          substitute_search('pizza2')[2].name],
                         ['pizza1', 'pizza3', 'pizza6'])
        self.assertEqual(substitute_search('pizza1')[0].name, 'pizza6')


class IndexPageTestCase(TestCase):
    '''Index page test class'''
    def test_index_page_returns_200(self):
        '''Test if the Http request returns 200'''
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mes_aliments/index.html')

    def test_register_favorite_ok(self):
        ''' Test if the products registration
            as favorite response returns 200 '''
        # Init one category and two products
        self.category = Category.objects.create(name='pizza')
        self.product1 = Product.objects.create(
                name='pizza1', brands='marque', nutriscore_grade='a',
                url='url', image='image', stores='magasin')
        self.product2 = Product.objects.create(
                name='pizza2', brands='marque', nutriscore_grade='a',
                url='url', image='image', stores='magasin')
        response = self.client.post(reverse('home'), data={'pk_prod': '1',
                                                           'pk_subs': '2'})
        self.assertEqual(response.status_code, 200)


class LegalMentionPageTestCase(TestCase):
    '''Legal Mention page test class'''
    def test_legal_mention_page_returns_200(self):
        '''Test if the Http request returns 200'''
        response = self.client.get(reverse('mention_legal'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mes_aliments/mention_legal.html')


class ProductPageTestCase(TestCase):
    '''Product page test class'''
    def test_product_page_returns_200(self):
        '''Test if the Http request returns 200
           and all substitute with a best nutriscore
           for the selected product '''
        # Init one category and one product
        self.category = Category.objects.create(name='pizza')
        self.product = Product.objects.create(
                name='pizza1', brands='marque', nutriscore_grade='a',
                url='url', image='image', stores='magasin')
        response = self.client.post('/mes_substituts/',
                                    data={'request_search': 'pizza'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mes_aliments/mes_produits.html')

    def test_product_page_returns_404(self):
        '''Test if the Http request returns 200
           and all substitute with a best nutriscore
           for the selected product '''
        # Init one category and one product
        self.category = Category.objects.create(name='pizza')
        self.product = Product.objects.create(
                name='pizza1', brands='marque', nutriscore_grade='a',
                url='url', image='image', stores='magasin')
        response = self.client.post('/mes_substituts/',
                                    data={'request_search': ''})
        self.assertEqual(response.status_code, 404)

    def test_exception_returns_404(self):
        ''' Test if the exception returns 404 '''
        # Init one category and two products
        self.category = Category.objects.create(name='pizza')
        self.product1 = Product.objects.create(
                name='pizza1', brands='marque', nutriscore_grade='a',
                url='url', image='image', stores='magasin')
        self.product2 = Product.objects.create(
                name='pizza2', brands='marque', nutriscore_grade='a',
                url='url', image='image', stores='magasin')
        response = self.client.post('/mes_substituts/',
                                    data={'request_search': 'dbbdé"bd'})
        self.assertEqual(response.status_code, 404)



class CreateAccountPageTestCase(TestCase):
    ''' Create Account page test class '''
    def test_create_page_returns_200(self):
        ''' Test of the Http request returns 200 '''
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/create.html')

    def test_create_account_ok(self):
        ''' Test of acccount creation '''
        response = self.client.post(reverse('create'), data={
            'email': 'i@i.com', 'username': 'iiii', 'password1': 'azeqsd00'})
        self.assertEqual(response.status_code, 200)


class LoginPageTestCase(TestCase):
    '''Login page test class'''
    def test_login_page_returns_200(self):
        '''Test of the Http request returns 200'''
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def setUp(self):
        '''Init all needed data to test the user's login'''
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        '''Test if the user is logged after the login step'''
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)


class AccountPageTestCase(TestCase):
    '''Account page test class'''
    def setUp(self):
        '''Init all needed data for the test'''
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        '''Test if the Http request returns 200 when the user is logged'''
        # send login data
        self.client.post('/login/', self.credentials, follow=True)
        response = self.client.get('/mon_compte/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mes_aliments/my_account.html')


class FavoritePageTestCase(TestCase):
    '''Favorite page test class'''
    def setUp(self):
        '''Init all needed data for the test'''
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_favorite_page_returns_200(self):
        '''Test if the Http request 200 when the user is logged'''
        self.client.post('/login/', self.credentials, follow=True)
        response = self.client.get('/mes_favoris/')
        self.assertEqual(response.status_code, 200)

    def test_template_favoris(self):
        self.client.post('/login/', self.credentials, follow=True)
        response = self.client.get('/mes_favoris/')
        self.assertTemplateUsed(response, 'mes_aliments/mes_favoris.html')


class ProductDetailPageTestCase(TestCase):
    ''' Product Detail page test class '''
    def test_detail_page_returns_200(self):
        '''Test if the Http request 200 '''
        # Init one category and one product
        self.category = Category.objects.create(name='pizza')
        self.product = Product.objects.create(
                name='pizza1', brands='marque', nutriscore_grade='a',
                url='url', image='image', stores='magasin')
        response = self.client.get(reverse('my_product',
                                           args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
