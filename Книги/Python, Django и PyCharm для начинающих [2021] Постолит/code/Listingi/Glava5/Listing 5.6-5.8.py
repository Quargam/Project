# Listing 5.6
def index(request):
    return render(request, "firstapp/home.html")


# Listing 5.7
from django.template.response import TemplateResponse


def index(request):
    return TemplateResponse(request, "firstapp/home.html")


# Listing 5.8
from django.shortcuts import render


def index(request):
    return render(request, "firstapp/home.html")
