# Listing 6.48
from django import forms


class UserForm(forms.Form):
    name = forms.CharField(label="Имя")
    age = forms.IntegerField(label="Возраст")
    email = forms.EmailField(label="Электронный адрес")
    reklama = forms.BooleanField(label="Согласны получать рекламу")


# Listing 6.49
from django.http import *
from .forms import UserForm
from django.shortcuts import render


def index(request):
    if request.method == "POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            name = userform.cleaned_data["name"]
            return HttpResponse("<h2>Имя введено коррректно – {0}</h2>".format(name))
        else:
            return HttpResponse("Ошибка ввода данных")
    else:
        userform = UserForm()
        return render(request, "firstapp/index.html", {"form": userform})
