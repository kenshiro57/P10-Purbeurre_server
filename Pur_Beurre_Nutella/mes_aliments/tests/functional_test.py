'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver import FirefoxOptions

# from ..models import Category, Contact, Product, Favorite

""" Django Functional Test with Selenium library """
"""" automatising user's interaction with the website """


class TestProject(LiveServerTestCase):
    ''' All functional Django Test class '''
    def setUp(self):
        ''' Init all Functional test '''
        # Path to edge webdriver
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        self.browser = webdriver.Firefox(firefox_options=opts)
        self.INDEX_PAGE_URL = 'http://127.0.0.1:8000/'
        self.LOGIN_PAGE_URL = 'http://127.0.0.1:8000/login/'
        self.CREATE_PAGE_URL = 'http://127.0.0.1:8000/create/'
        self.PRODUCT_DETAIL_URL = 'http://127.0.0.1:8000/mon_produit/1/'

    def test_index_page_title(self):
        ''' Little functional test to make sure about the url page contents '''
        # Get the selected page contents
        self.browser.get(self.INDEX_PAGE_URL)
        # Test comparison between the current url and the test's expected url
        self.assertEqual(self.browser.title, 'Pur-Beurre')
        # Stop the program for 1 second
        time.sleep(1)
        # Close the current page
        self.browser.quit()

    def test_login(self):
        ''' Login functional Test '''
        self.browser.get(self.LOGIN_PAGE_URL)
        # Search the Html element by id and input the value
        self.browser.find_element_by_id(
            "id_username").send_keys('iii')
        self.browser.find_element_by_id(
                "id_password").send_keys('azeqsd00')
        # Click button event
        self.browser.find_element_by_id("registration_button").click()
        time.sleep(5)
        self.assertEqual(self.browser.current_url, self.INDEX_PAGE_URL)
        time.sleep(1)
        self.browser.quit()

    def test_account_create(self):
        ''' Account creation functional test '''
        self.browser.get(self.CREATE_PAGE_URL)
        self.browser.find_element_by_id("id_username").send_keys('iii')
        self.browser.find_element_by_id("id_email").send_keys('i@i.com')
        self.browser.find_element_by_id("id_password1").send_keys('azeqsd00')
        self.browser.find_element_by_id("id_password2").send_keys('azeqsd00')
        self.browser.find_element_by_id("registration_button").click()
        self.assertEqual(self.browser.current_url, self.LOGIN_PAGE_URL)
        self.browser.quit()

    def test_product_detail(self):
        ''' Detail page functionnal test '''
        self.browser.get(self.INDEX_PAGE_URL)
        self.browser.find_element_by_id("text_input").send_keys('pizza')
        self.browser.find_element_by_id("button").click()
        self.browser.find_element_by_id("//img[@id='fav_img']").click()
        self.assertEqual(self.browser.current_url, self.PRODUCT_DETAIL_URL)
