# Listing 6.1
from django import forms


class UserForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField()


# Listing 6.2
from django.shortcuts import render
from .forms import UserForm


def index(request):
    userform = UserForm()
    return render(request, "firsatapp/index.html",
                  {"form": userform})
