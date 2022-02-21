# Listing 7.10
from django.urls import path
from firstapp import views

urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    path('edit/<int:id>/', views.edit),
    path('delete/<int:id>/', views.delete),
]

# Listing 7.11
from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    objects = models.Manager()
    DoesNotExist = models.Manager


class Company(models.Model):
    name = models.CharField(max_length=30)


class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    price = models.IntegerField()


# Listing 7.12
# создаем объект Company с именем Электрон
firma = Company.objects.create(name=" Электрон")

# создание товара компании
firma.product_set.create(name="Samsung S20", price=42000)

# отдельное создание объекта с последующим добавлением в БД
ipad = Product(name="iPad", price=34200)
# при добавлении необходимо указать параметр bulk =False
firma.product_set.add(ipad, bulk=False)

# исключает из компании все товары,
# при этом товары остаются в БД и не привязаны к компании
# работает, если в зависимой модели ForeignKey(Company, null = True)
# firma.product_set.clear()

# то же самое, только в отношении одного объекта
# ipad = Product.objects.get(name="iPad")
# firma.product_set.remove(ipad)


# Listing 7.13
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=30)


class Student(models.Model):
    name = models.CharField(max_length=30)
    courses = models.ManyToManyField(Course)


# Listing 7.14
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=20)


class Account(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


