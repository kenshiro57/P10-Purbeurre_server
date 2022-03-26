from . import *
import raven

SECRET_KEY = '#+3^0gumy+=ykmr_rx2i2uo1hgzu-4nxj*pm$4^3vx7v-7v#l1'
DEBUG = False
ALLOWED_HOSTS = ['192.241.138.251']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'purbeurre',
        'USER': 'ihsan',
        'PASSWORD': 'salman57',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'NAME': 'purbeurre',    
            },
    }
}
