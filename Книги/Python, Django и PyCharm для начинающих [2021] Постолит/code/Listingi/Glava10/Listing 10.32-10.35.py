# Listing 10.32
path('edit1/<int:id>/', views.edit1, name='edit1'),
path('create/', views.create, name='create'),
path('delete/<int:id>/', views.delete, name='delete'),

# Listing 10.33
from django.forms import ModelForm
from .models import Book


class BookModelForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'language', 'author', 'summary', 'isbn']


# Listing 10.34
fields = [' summary', ]
labels = {' summary ': _('Аннотация'), }
help_texts = {' summary ': _('Не более 1000 символов'), }

# Listing 10.35
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book


class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
