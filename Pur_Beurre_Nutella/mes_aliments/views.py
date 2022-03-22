'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.http import HttpResponse
from django.shortcuts import render, redirect  # , get_object_or_404
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from sentry_sdk import capture_message

from .models import Product, Favorite, Contact
from .helper.function import substitute_search, product_search
from .forms import RegisterForm, CustomAuthenticationForm


@csrf_exempt
def index(request):
    ''' return index template'''
    template = loader.get_template('mes_aliments/index.html')
    if request.method == 'POST':
        product_id = request.POST.get("pk_prod")
        substitute_id = request.POST.get('pk_subs')
        favorite_registered = Favorite.objects.filter(
            product_id=product_id, substitute_id=substitute_id)
        if not favorite_registered.exists():
            username = request.user.username
            favorite = Favorite.objects.create(
                product_id=product_id,
                substitute_id=substitute_id,
                username=username)
            favorite.save()
    return HttpResponse(template.render(request=request))


@csrf_exempt
def product(request):
    '''get the user's query and return the related product'''
    template = loader.get_template('mes_aliments/mes_produits.html')
    try:
        if request.method == 'POST':
            search_request = request.POST.get('request_search')
            if search_request == '':
                return render(request, 'error_page/404.html', status=404)
            my_product = product_search(search_request)[0]
            substitutes = substitute_search(search_request)
        context = {'product': my_product,
                   'substitutes': substitutes}
    except IndexError:
        return render(request, 'error_page/404.html', status=404)
    return HttpResponse(template.render(context, request=request))


def detail_product(request, pk):
    '''get the pk of the product and return the detail of the product'''
    template = loader.get_template('mes_aliments/mon_produit.html')
    if request.method == 'GET':
        product_detail = Product.objects.filter(id=pk)
    context = {'product': product_detail[0]}
    return HttpResponse(template.render(context, request=request))


def legal_mention(request):
    '''return legal mention template'''
    template = loader.get_template('mes_aliments/mention_legal.html')
    return HttpResponse(template.render(request=request))


@login_required(login_url='/login/')
def my_favorite(request):
    '''return the template of the favorites'''
    favorite_product = []
    favorite_substitute = []
    template = loader.get_template('mes_aliments/mes_favoris.html')
    if request.method == 'GET':
        favorites = Favorite.objects.filter(username=request.user.username)
        for favorite in favorites:
            product_fav = Product.objects.filter(id=favorite.product_id)
            favorite_product.append(product_fav[0])
            substitute = Product.objects.filter(id=favorite.substitute_id)
            favorite_substitute.append(substitute[0])
    context = {'favorite_product': favorite_product,
               'favorite_substitute': favorite_substitute}
    return HttpResponse(template.render(context, request=request))


def create(request):
    '''return the template to create an user account
       and add in the database all related information'''
    context = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            name = request.POST.get('username')
            password = make_password(request.POST.get('password1'))
            contact = Contact.objects.filter(email=email)
            if not contact.exists():
                # If a contact is not registered, create a new one.
                user = User.objects.create(
                    username=name,
                    email=email,
                    password=password
                )
                contact = Contact.objects.create(email=email, name=name)
                user.save()
                contact.save()
            else:
                contact = contact.first()

            return redirect('/login/')
        else:
            # Form data doesn't match the expected format.
            # Add errors to the template.
            context['errors'] = form.errors.items()
    else:
        form = RegisterForm()
    return render(request, 'registration/create.html', {'form': form})


@login_required(login_url='/login/')
def my_account(request):
    '''return the template of user's personal informations'''
    template = loader.get_template('mes_aliments/my_account.html')
    return HttpResponse(template.render(request=request))


class CustomLoginView(LoginView):
    '''Custimize the login view to change
       the default username label to email'''
    authentication_form = CustomAuthenticationForm


def page_not_found(request, exception):
    '''return the 404 error page'''
    capture_message("Page not found!", level="error")
    return render(request, 'error_page/404.html', status=404)


def server_error(request):
    '''return the 500 error page'''
    return render(request, 'error_page/500.html', status=500)
