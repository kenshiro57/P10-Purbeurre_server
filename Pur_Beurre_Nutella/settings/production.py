from . import *

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
    }
}
sentry_sdk.init(
    dsn = "https://27109c567d1042a184be83af0aa3d57b@o1039948.ingest.sentry.io/6008793",
    integrations = [DjangoIntegration()],
    traces_sample_rate  = 1.0,
    send_default_pii = True
    )
