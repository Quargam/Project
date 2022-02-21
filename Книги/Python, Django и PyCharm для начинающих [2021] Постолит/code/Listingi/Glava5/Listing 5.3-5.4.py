# Listing 5.3
from django.shortcuts import render


def index(request):
    return render(request, "index.html")


# Listing 5.4
from django.contrib import admin
from django.urls import path
from firstapp import views

urlpatterns = [
    path('', views.index),
]

