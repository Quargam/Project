# Listing 9.16
class BookListView(generic.ListView):
    model = Book
    paginate_by = 3
