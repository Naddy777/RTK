from django import forms
from .validators import russian_email
from django.core.validators import MinLengthValidator

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100,
                           validators=[MinLengthValidator(2)], # список всех валидаторов можно найти на сайте djangodoc.ru валидаторы
                           initial='') # можно прописать текст в поле
    email = forms.EmailField(validators=[russian_email])
    message = forms.CharField(widget=forms.Textarea)
    demo = forms.BooleanField(required = False, help_text='Поставьте галочку, если вам нравится наш сайт', label='Вам нравится наш сайт?', initial=True) # по умолчанию True

# required = False - ставим у того поля, которое необязательно для заполнения, т.е. может быть пустым
# initial=True - ставим, если уже надо заполнить поле, т.е. поставить галочку
# disabled=True - ставим, если поле надо деактивировать
