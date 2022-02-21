# Listing 6.57
from django import forms


class UserForm(forms.Form):
    name = forms.CharField(label="Имя клиента", min_length=3)
    age = forms.IntegerField(label="Возраст клиента", min_value=1, max_value=100)
    required_css_class = "field"
    error_css_class = "error"
