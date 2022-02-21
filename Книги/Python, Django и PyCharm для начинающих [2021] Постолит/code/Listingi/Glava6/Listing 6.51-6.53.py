# Listing 6.51
from django import forms


class UserForm(forms.Form):
    name = forms.CharField(label="Имя")


# Listing 6.52
from django import forms


class UserForm(forms.Form):
    name = forms.CharField(label="Имя клиента")
    age = forms.IntegerField(label="Возраст клиента")


# Listing 6.53
from django.http import *
from .forms import UserForm
from django.shortcuts import render


def index(request):
    userform = UserForm()
    if request.method == "POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            name = userform.cleaned_data["name"]
            return HttpResponse("<h2>Имя введено коррректно – {0}</h2>".format(name))
    return render(request, "firstapp/index.html", {"form": userform})
