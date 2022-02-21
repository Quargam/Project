# Листинг 2.16
# Класс кошки
class Cat:
    Name_Class = "Кошки"

    # Действия, которые надо выполнять при создании объекта "Кошка"
    def __init__(self, wool_color, eyes_color, name):
        self.wool_color = wool_color
        self.eyes_color = eyes_color
        self.name = name

    # Мурлыкать
    def purr(self):
        print("Муррр!")

    # Шипеть
    def hiss(self):
        print("Шшшш!")

    # Царапаться
    def scrabble(self):
        print("Цап-царап!")


# Листинг 2.17
class Cat:
    Name_Class = "Кошки"

    # Действия, которые надо выполнять при создании объекта "Кошка"
    def __init__(self, wool_color, eyes_color, name):
        self.wool_color = wool_color
        self.eyes_color = eyes_color
        self.name = name


# Листинг 2.18
Сlass Cat:
    Name_Class = "Кошки"

    # Действия, которые надо выполнять при создании объекта "Кошка"
    def __init__(self, wool_color, eyes_color, name):
        self.wool_color = wool_color
        self.eyes_color = eyes_color
        self.name = name

    # Мурлыкать
    def purr(self):
        print("Муррр!")

    # Шипеть
    def hiss(self):
        print("Шшшш!")

    # Царапаться
    def scrabble(self):
        print("Цап-царап!")

# Листинг 2.19
my_cat = Cat('Белая', 'Зеленые', 'Мурка')
print("Наименование класса - ", my_cat.Name_Class)
print("Вот наша кошка:")
print("Цвет шерсти- ", my_cat.wool_color)
print("Цвет глаз- ", my_cat.eyes_color)
print("Кличка- ", my_cat.name)

# Листинг 2.20
my_cat = Cat('Белая', 'Зеленые', 'Мурка')
my_cat.name = "Васька"
my_cat.wool_color = "Черный"
print("Наименование класса - ", my_cat.Name_Class)
print("Вот наша кошка:")
print("Цвет шерсти- ", my_cat.wool_color)
print("Цвет глаз- ", my_cat.eyes_color)
print("Кличка- ", my_cat.name)

# Листинг 2.21
class Car(object):
    # Наименование класса
    Name_class = "Автомобиль"

    def __init__(self, brand, weight, power):
        self.brand = brand    # Марка, модель автомобиля
        self.weight = weight  # Вес автомобиля
        self.power = power    # Мощность двигателя

        # Метод двигаться прямо

    def drive(self):
        # Здесь команды двигаться прямо
        print("Поехали, двигаемся прямо!")

        # Метод повернуть на право

    def righ(self):
        # Здесь команды повернуть руль направо
        print("Едем, поворачиваем руль направо!")

        # Метод повернуть на лево

    def left(self):
        # Здесь команды повернуть руль налево
        print("Едем, поворачиваем руль налево!")

        # Метод тормозить

    def brake(self):
        # Здесь команды нажатия на педаль тормоза
        print("Стоп, активируем тормоз")

    # Метод подать звуковой сигналь
    def beep(self):
        # Здесь команды подачи звукового сигнала
        print("Подан звуковой сигнал")

# Листинг 2.22
MyCar = Car('Мерседес', 1200, 250)
print('Параметры автомобиля, созданного из класса- ', MyCar.Name_class)
print('Марка (модель)- ', MyCar.brand)
print('Вес (кг)- ', MyCar.weight)
print('Мощность двигателя (лс)- ', MyCar.power)

# Листинг 2.23
MyCar.drive()   # Двигается прямо
MyCar.righ()    # Поворачиваем направо
MyCar.drive()   # Двигается прямо
MyCar.left()    # Поворачиваем налево
MyCar.drive()   # Двигается прямо
MyCar.beep()    # Подаем звуковой сигнал
MyCar.brake()   # Тормозим
