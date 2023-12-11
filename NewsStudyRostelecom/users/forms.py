from django import forms
from .validators import russian_email
from django.core.validators import MinLengthValidator
from .models import Account
from django.forms import TextInput, EmailInput, FileInput, Select
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User



class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {'username': TextInput({'class': 'textinput form-control',
                                          'placeholder': 'username'}),
                   'email': EmailInput({'class': 'textinput form-control',
                                        'placeholder': 'email'}),
                   'first_name': TextInput({'class': 'textinput form-control',
                                            'placeholder': 'First name'}),
                   'last_name': TextInput({'class': 'textinput form-control',
                                           'placeholder': 'Last name'}),
                   }

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['phone', 'firstname','lastname','address','vk','telegram', 'account_image']
        widgets = {'phone': TextInput({'class': 'textinput form-control',
                                       'placeholder': 'phone number'}),
                   'address': TextInput({'class': 'textinput form-control',
                                         'placeholder': 'address'}),
                   'firstname': TextInput({'class': 'textinput form-control',
                                         'placeholder': 'address'}),
                   'lastname': TextInput({'class': 'textinput form-control',
                                         'placeholder': 'address'}),
                   'vk': TextInput({'class': 'textinput form-control',
                                      'placeholder': 'vk'}),
                   'telegram': TextInput({'class': 'textinput form-control',
                                           'placeholder': 'telegram'}),
                   'account_image': FileInput({'class': 'form-control',
                                       'placeholder': 'image'})
                   }
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
