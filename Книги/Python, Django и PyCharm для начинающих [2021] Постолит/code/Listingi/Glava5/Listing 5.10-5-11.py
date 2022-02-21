# Listing 5.10
def index(request):
    # return render(request, "firstapp/home.html")
    data = {"header": "Передача параметров в шаблон Django",
            "message": "Загружен шаблон templates/firstapp/index_app1.html"}
    return render(request, "firstapp/index_app1.html", context=data)


# Listing 5.11
def index(request):
    header = "Персональные данные"  # обычная переменная
    langs = ["Английский", "Немецкий", "Испанский"]  # массив
    user = {"name": "Максим,", "age": 30}  # словарь
    addr = ("Виноградная", 23, 45)  # кортеж
    data = {"header": header, "langs": langs, "user": user, "address": addr}
    return render(request, "index.html", context=data)

# Listing 5.8
