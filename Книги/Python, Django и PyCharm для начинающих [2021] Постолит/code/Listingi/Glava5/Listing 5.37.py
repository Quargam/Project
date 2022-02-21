# Listing 5.37
from django.http import *
from django.shortcuts import render


def index(request):
    data = {"age": 50}
    return render(request, "firstapp/index.html", context=data)
