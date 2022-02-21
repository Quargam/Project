# Listing 8.1
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Главная страница сайта  Мир книг!")


# Listing 8.2
from django.contrib import admin
from django.urls import path
from catalog import views

urlpatterns = [
    path('', views.index, name='home'),
    path('admin/', admin.site.urls),
]


# Listing 8.3
class Genre(models.Model):
    name = models.CharField(max_length=200,
                            help_text=" Введите жанр книги", verbose_name="Жанр книги")

    def __str__(self):
        return self.name


# Listing 8.4
class Language(models.Model):
    name = models.CharField(max_length=20,
                            help_text=" Введите язык книги", verbose_name="Язык книги")

    def __str__(self):
        return self.name


# Listing 8.5
class Author(models.Model):
    first_name = models.CharField(max_length=100, help_text="Введите имя автора",
                                  verbose_name="Имя автора")
    last_name = models.CharField(max_length=100, help_text="Введите фамилию автора",
                                 verbose_name="Фамилия автора")
    date_of_birth = models.DateField(help_text="Введите дату рождения", verbose_name="Дата рождения",
                                     null=True, blank=True)
    date_of_death = models.DateField(help_text="Введите дату смерти", verbose_name="Дата смерти",
                                     null=True, blank=True)

    def __str__(self):
        return self.last_name


# Listing 8.6
class Book(models.Model):
    title = models.CharField(max_length=200,
                             help_text="Введите название книги",
                             verbose_name="Название книги")
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE,
                              help_text=" Выберите жанр для книги",
                              verbose_name="Жанр книги", null=True)
    language = models.ForeignKey('Language',
                                 on_delete=models.CASCADE,
                                 help_text="Выберите язык книги",
                                 verbose_name="Язык книги", null=True)
    author = models.ManyToManyField('Author',
                                    help_text="Выберите автора книги",
                                    verbose_name="Автор книги", null=True)
    summary = models.TextField(max_length=1000,
                               help_text="Введите краткое описание книги",
                               verbose_name="Аннотация книги")
    isbn = models.CharField(max_length=13,
                            help_text="Должно содержать 13 символов",
                            verbose_name="ISBN книги")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Возвращает url-адрес для доступа к определенному экземпляру книги.
        return reverse('book-detail', args=[str(self.id)])


# Listing 8.7
class Status(models.Model):
    name = models.CharField(max_length=20,
                            help_text="Введите статус экземпляра книги",
                            verbose_name="Статус экземпляра книги")

    def __str__(self):
        return self.name


# Listing 8.8
class BookInstance(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE,
                             null=True)
    inv_nom = models.CharField(max_length=20, null=True,
                               help_text="Введите инвентарный номер экземпляра",
                               verbose_name="Инвентарный номер")
    imprint = models.CharField(max_length=200,
                               help_text="Введите издательство и год выпуска",
                               verbose_name="Издательство")
    status = models.ForeignKey('Status', on_delete=models.CASCADE,
                               null=True,
                               help_text='Изменить состояние экземпляра',
                               verbose_name="Статус экземпляра книги")
    due_back = models.DateField(null=True, blank=True,
                                help_text="Введите конец срока статуса",
                                verbose_name="Дата окончания статуса")

    def __str__(self):
        return '%s %s %s' % (self.inv_nom, self.book, self.status)


# Listing 8.9
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')


# Listing 8.10
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'display_author')


# Listing 8.11
def display_author(self):
    return ', '.join([author.last_name for author in self.author.all()])


display_author.short_description = 'Авторы'


# Listing 8.12
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'display_author')
    list_filter = ('genre', 'author')


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('book', 'status')


# Listing 8.13
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    fields = ['first_name', 'last_name',
             ('date_of_birth', 'date_of_death')]


# Listing 8.14
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('book', 'status')
    fieldsets = (
        ('Экземпляр книги', {
            'fields': ('book', 'imprint', 'inv_nom')
        }),
        ('Статус и окончание его действия', {
            'fields': ('status', 'due_back')
        }),
    )


# Listing 8.15
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]
