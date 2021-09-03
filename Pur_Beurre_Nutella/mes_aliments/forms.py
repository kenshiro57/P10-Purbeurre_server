'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class RegisterForm(UserCreationForm):
    '''Register form class'''
    email = forms.EmailField()

    class Meta:
        '''Making line between the form and User model'''
        model = User
        fields = ["username", "email", "password1", "password2"]


class EmailBackend(ModelBackend):
    '''change username authentification to email'''
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(Q(username__iexact=username) |
                                         Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        except MultipleObjectsReturned:
            return User.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(
               user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None


class CustomAuthenticationForm(AuthenticationForm):
    '''change username label in login form to email label'''
    username = UsernameField(
        label='Email',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
