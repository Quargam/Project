# Listing 9.8
context = {'num_books': num_books,
           'num_instances': num_instances,
           'num_instances_available': num_instances_available,
           'num_authors': num_authors}

# Listing 9.9
from django.contrib import admin
from django.urls import path
from catalog import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
]

# Listing 9.10
from django.views import generic


class BookListView(generic.ListView):
    model = Book


