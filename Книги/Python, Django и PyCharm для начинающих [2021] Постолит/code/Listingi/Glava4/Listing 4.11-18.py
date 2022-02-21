# Listing 4.11
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from firstapp import views

urlpatterns = [
    path('', views.index),
    re_path(r'^about', views.about),
    re_path(r'^contact', views.contact),
    path('products/<int:productid>/', views.products),
    path('users/<int:id>/<name>/', views.users),
]


# Listing 4.12
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h2>Главная</h2>")

def about(request):
    return HttpResponse("<h2>О сайте</h2>")

def contact(request):
    return HttpResponse("<h2>Контакты</h2>")

def products(request, productid=1):
    output = "<h2>Продукт № {0}</h2>".format(productid)
    return HttpResponse(output)

def users(request, id=1, name=”Максим”):
    output = "<h2>Пользователь</h2><h3>id: {0}
                  Имя: {1}</h3>".format(id, name)
    return HttpResponse(output)



# Listing 4.13
path('products/', views.products), # маршрут по умолчанию
path('products/<int:productid>/', views.products),
path('users/', views.users), # маршрут по умолчанию
path('users/<int:id>/<str:name>/', views.users),



# Listing 4.14
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from firstapp import views

urlpatterns = [
    path('', views.index),
    re_path(r'^about', views.about),
    re_path(r'^contact', views.contact),
    path('products/', views.products),  # маршрут по умолчанию
    path('products/<int:productid>/', views.products),
    path('users/', views.users),  # маршрут по умолчанию
    path('users/<int:id>/<str:name>/', views.users),
]


# Listing 4.15
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h2>Главная</h2>")

def about(request):
    return HttpResponse("<h2>О сайте</h2>")

def contact(request):
    return HttpResponse("<h2>Контакты</h2>")

def products(request, productid):
    category = request.GET.get("cat", "")
    output = "<h2>Продукт № {0}  Категория: {1}</h2>" .format(productid, category)
    return HttpResponse(output)

def users(request):
    id = request.GET.get("id", 1)
    name = request.GET.get("name", "Максим")
    output = "<h2>Пользователь</h2><h3>id: {0}  Имя: {1}</h3 >" .format(id, name)
    return HttpResponse(output)



# Listing 4.16
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from firstapp import views

urlpatterns = [
    path('', views.index),
    re_path(r'^about', views.about),
    re_path(r'^contact', views.contact),
    path('products/<int:productid>/', views.products),
    path('users/', views.users),
]



# Listing 4.17
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect


def index(request):
    return HttpResponse("Index")


def about(request):
    return HttpResponse("About")


def contact(request):
    return HttpResponseRedirect("/about")


def details(request):
    return HttpResponsePermanentRedirect("/")


# Listing 4.18
from django.urls import path
from firstapp import views

urlpatterns = [
    path('', views.index),
    path('about/', views.about),
    path('contact/', views.contact),
    path('details/', views.details),
]


