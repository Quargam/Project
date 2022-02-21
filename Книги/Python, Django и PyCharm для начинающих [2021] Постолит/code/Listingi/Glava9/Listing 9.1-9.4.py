# Listing 9.1
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

# Listing 9.2
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Главная страница сайта  Мир книг!")


# Listing 9.3
from .models import Book, Author, BookInstance, Genre


# Listing 9.4
def index(request):
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'На складе')
    # Здесь метод 'all()' применен по умолчанию.
    num_instances_available = BookInstance.objects.filter(status__exact=2).count()
    # Авторы книг,
    num_authors = Author.objects.count()

    # Отрисовка HTML-шаблона index.html с данными
    # внутри переменной context
    return render(request, 'index.html', context={
                                         'num_books': num_books,
                                         'num_instances': num_instances,
                                         'num_instances_available': num_instances_available,
                                         'num_authors': num_authors,
                                         'num_visits': num_visits})
