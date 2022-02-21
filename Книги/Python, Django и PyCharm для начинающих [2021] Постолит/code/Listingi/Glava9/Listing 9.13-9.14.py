# Listing 9.13
from django.contrib import admin
from django.urls import path
from catalog import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
]


# Listing 9.14
class BookDetailView(generic.DetailView):
    model = Book



