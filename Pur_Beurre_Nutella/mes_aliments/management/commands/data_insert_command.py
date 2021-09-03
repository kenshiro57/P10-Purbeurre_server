'''!/usr/bin/python3
   -*- coding: Utf-8 -'''

from django.core.management.base import BaseCommand

from ...data import PsqlData


class Command(BaseCommand):
    '''Command class'''
    args = '<team_id>'
    help = 'Affiche la liste des backlogs'

    def handle(self, *args, **options):
        '''return the instance of the imported class'''
        self.psql_data = PsqlData()
