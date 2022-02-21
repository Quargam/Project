# Listing 6.8
from .forms import UserForm
from django.shortcuts import render


def index(request):
    userform = UserForm()
    return render(request, "firstapp/index.html", {"form": userform})


# Listing 6.9
from django import forms


class UserForm(forms.Form):
    name = forms.CharField(label="Имя клиента")
    age = forms.IntegerField(label="Возраст клиента")


# Listing 6.10
from django import forms
class UserForm(forms.Form):
basket = forms.BooleanField(label="Положить товар в корзину")


# Listing 6.11
from django import forms
class UserForm(forms.Form):
basket = forms.BooleanField(label="Положить в корзину", required=False)


# Listing 6.12
from django import forms
class UserForm(forms.Form):
    vyb = forms.NullBooleanField(label="Вы поедете в Сочи этим летом?")


# Listing 6.13
from django import forms
class UserForm(forms.Form):
   name = forms.CharField(label="Имя клиента")


# Listing 6.14
from django import forms
class UserForm(forms.Form):
   email = forms.EmailField(label="Электронный адрес", help_text="Обязательный символ - @")


# Listing 6.15
from django import forms
class UserForm(forms.Form):
   ip_adres = forms.GenericIPAddressField(label="IP адрес", help_text=" Пример формата 192.0.2.0")


# Listing 6.16
from django import forms
class UserForm(forms.Form):
   reg_text = forms.RegexField(label="Текст", regex="^[0-9][A-F][0-9]$")


# Listing 6.17
from django import forms
class UserForm(forms.Form):
   slug_text = forms.SlugField(label="Введите текст")


# Listing 6.18
from django import forms
class UserForm(forms.Form):
   url_text = forms.URLField(label="Введите URL", help_text="Например http://www.google.com")


# Listing 6.19
from django import forms
class UserForm(forms.Form):
   uuid_text = forms.UUIDField(label="Введите UUID", help_text="Формат xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")


# Listing 6.20
from django import forms
class UserForm(forms.Form):
   combo_text = forms.ComboField(label="Введите URL",
                                fields=[forms.URLField(), forms.CharField(max_length=20)])


# Listing 6.21
from django import forms
class UserForm(forms.Form):
    file_path = forms.FilePathField(label="Выберите файл", path="C:/Python37/")


# Listing 6.22
from django import forms
class UserForm(forms.Form):
    file_path = forms.FilePathField(label="Выберите файл", path="C:/Python37/",
                                    allow_files="True", allow_folders="True")


# Listing 6.23
from django import forms
class UserForm(forms.Form):
    file = forms.FileField(label="Файл")


# Listing 6.24
from django import forms
class UserForm(forms.Form):
    file = forms.ImageField(label="Изображение")


# Listing 6.25
from django import forms
class UserForm(forms.Form):
    date = forms.DateField(label="Введите дату")


# Listing 6.26
from django import forms
class UserForm(forms.Form):
    time = forms.DateField(label="Введите время")


# Listing 6.27
from django import forms
class UserForm(forms.Form):
    date_time = forms.DateTimeField(label="Введите дату и время")


# Listing 6.28
from django import forms
class UserForm(forms.Form):
    time_delta = forms.DurationField(label="Введите промежуток времени")


# Listing 6.29
from django import forms
class UserForm(forms.Form):
    date_time = forms.SplitDateTimeField(label="Введите дату и время")


# Listing 6.30
from django import forms
class UserForm(forms.Form):
    num = forms.IntegerField(label="Введите целое число")


# Listing 6.31
from django import forms
class UserForm(forms.Form):
    num = forms.DecimalField(label="Введите десятичное число")


# Listing 6.32
from django import forms
class UserForm(forms.Form):
    num = forms.DecimalField(label="Введите десятичное число", decimal_places=2)


# Listing 6.33
from django import forms
class UserForm(forms.Form):
    num = forms.FloatField(label="Введите число")


# Listing 6.34
ffrom django import forms
class UserForm(forms.Form):
    ling = forms.ChoiceField(label="Выберите язык",
                             choices=((1, "Английский"),
                                      (2, "Немецкий"),
                                      (3, "Французский")))


# Listing 6.35
from django import forms
class UserForm(forms.Form):
    city = forms.TypedChoiceField(label="Выберите город",
                                  empty_value=None,
                                  choices=((1, "Москва"),
                                           (2, "Воронеж"),
                                           (3, "Курск")))

# Listing 6.36
from django import forms
class UserForm(forms.Form):
    country = forms.MultipleChoiceField(label="Выберите страны",
                                        choices=((1, "Англия"),
                                                 (2, "Германия"),
                                                 (3, "Испания"),
                                                 (4, "Россия")))


# Listing 6.37
from django import forms
class UserForm(forms.Form):
    city = forms.TypedMultipleChoiceField(label="Выберите город",
                                          empty_value=None,
                                          choices=((1, "Москва"),
                                                   (2, "Воронеж"),
                                                   (3, "Курск"),
                                                   (4, "Томск")))

# Listing 6.38
from django import forms
class UserForm(forms.Form):
    name = forms.CharField(label="Имя")
    age = forms.IntegerField(label="Возраст")
    comment = forms.CharField(label="Комментарий")


# Listing 6.39
from django import forms
class UserForm(forms.Form):
    name = forms.CharField(label="Имя")
    age = forms.IntegerField(label="Возраст")
    comment = forms.CharField(label="Комментарий",
                              widget=forms.Textarea)


# Listing 6.40
from django import forms
class UserForm(forms.Form):
    name = forms.CharField(label="Имя", initial="Введите ФИО")
    age = forms.IntegerField(label="Возраст", initial=18)
    comment = forms.CharField(label="Комментарий", widget=forms.Textarea)


# Listing 6.41
from django import forms
class UserForm(forms.Form):
    name = forms.CharField(label="Имя", initial="Введите ФИО")
    age = forms.IntegerField(label="Возраст", initial=18)
    field_order = ["age", "name"]


# Listing 6.42
from django.http import *
from .forms import UserForm
from django.shortcuts import render

def index(request):
    userform = UserForm(field_order=["age", "name"])
    return render(request, "firstapp/index.html", {"form": userform})


# Listing 6.43
from django import forms
class UserForm(forms.Form):
    name = forms.CharField(label="Имя", initial="Введите ФИО")
    age = forms.IntegerField(label="Возраст", initial=18)


# Listing 6.44
from django.http import *
from .forms import UserForm
from django.shortcuts import render

def index(request):
    userform = UserForm()
    return render(request, "firstapp/index.html", {"form": userform})


# Listing 6.45
from django import forms
class UserForm(forms.Form):
    name = forms.CharField(label="Имя", help_text ="Введите ФИО")
    age = forms.IntegerField(label="Возраст", help_text ="Введите возраст")


