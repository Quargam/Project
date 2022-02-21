# Листинг 3.1
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):


# Листинг 3.2
from django.contrib import admin
from django.urls import path
from firstapp import views

urlpatterns = [
    path('', views.index, name='home'),
    path('admin/', admin.site.urls),
]
