from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import News, Product
def index (request):
#     value = -10
#     n1 = News('Новость 1', 'Текст 1', '07.11.23')
#     n2 = News('Новость 2', 'Текст 1', '07.11.23')
#     l = [n1, n2]
#     m = ['раз', 'два', 'три']
#     context = {'title': 'Мой сайт',
#             'Header1': 'Заголовок страницы',
#                'value': value,
#                'numbers': l,
#                'numbers2': m,
#                }
#     colors = ['red', 'blue', 'golden', 'black']
#     context1 = {
#         'colors': colors
#     }
    if request.method == 'POST':
        print('Получили post-запрос')
        print(request.POST)
        title = request.POST.get('title')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        new_product = Product(title,float(price),int(quantity))
        print('Создан товар: ', new_product.title, 'Общая сумма: ',new_product.amount())
    else:
        print('Получили get-запрос')

    water = Product('Добрый сок',40, 2)
    chocolate = Product('Шоколад', 30, 1)
    colors = ['red', 'blue','golden','black']
    context = {
        'colors': colors,
        'water': water,
        'chocolate': chocolate,
    }
    return render(request, 'main/index.html', context)
def contacts (request):
    return HttpResponse('<h1> Контакты </h1>')
def about (request):
    return HttpResponse('<h1> О нас </h1>')
def sidebar (request):
    return render(request, 'main/sidebar.html')

def test_page (request):
    return render(request, 'main/test_page.html')

def get_demo(request,a,operation,b):
    if operation == 'minus':
            result = int(a) - int (b)
    elif operation == 'plus':
            result = int(a) + int(b)
    elif operation == 'multiply':
            result = int(a) * int(b)
    elif operation == 'divide':
            result = int(a) / int(b)
    else:
            return HttpResponse('Неверная команда')
    return HttpResponse(f'Вы ввели: {a} и {b} <br> Результат: {operation}:{result}')

def custom_404(request,exception):
    return HttpResponse(f'Страница не найдена. Код ошибки:  {exception}')