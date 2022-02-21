# Listing 6.6
from django.http import *
from .forms import UserForm
from django.shortcuts import render


def index(request):
    if request.method == "POST":
        name = request.POST.get("name")  # получить значения поля Имя
        age = request.POST.get("age")  # значения поля Возраст
        output = "<h2>Пользователь</h2><h3>Имя - {0}, Возраст – {1}</h3>".format(name, age)
        return HttpResponse(output)
    else:
        userform = UserForm()
        return render(request, "firstapp/index.html", {"form": userform})
