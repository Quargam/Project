# Listing 2.6
def MyPrint(d, r):
    print('В функции мы выполнили печать ', d, 'переменных X и Y')
    print('Результат Z=', r)


# Listing 2.7
x = 2
y = 3
z = x + y
MyPrint('сложения', z)
z = x - y
MyPrint('вычитания', z)
z = x * y
MyPrint('умножения', z)
z = x / y
MyPrint('деления', z)
z = x ** y
MyPrint('возведения в степень', z)
