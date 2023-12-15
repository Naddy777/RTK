from django import forms
from django.core.validators import MinLengthValidator
from .models import *
from django.forms import ModelForm, Textarea, CheckboxSelectMultiple
from django.forms import TextInput, EmailInput, FileInput, Select

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

# from django.forms import inlineformset_factory
# ImagesFormSet = inlineformset_factory(Article, Image, fields=("image",),extra=1,max_num=4,
#     widgets={
#         "image_field": MultipleFileField(),
#     })

class ArticleForm(ModelForm):
    image_field = MultipleFileField()
    class Meta:
        model = Article
        fields = ['title','anouncement','text','tags','category']
        widgets = {
            'anouncement': Textarea(attrs={'cols':80,'rows':2}),
            'text': Textarea(attrs={'cols': 80, 'rows': 2}),
            'tags': CheckboxSelectMultiple(),
            # 'image': N ),
        }

class ArticleUpdateForm (forms.ModelForm):
    image_field = MultipleFileField(required=False)
    class Meta:
        model = Article
        fields = ['title','anouncement','text','tags','category', ]
        widgets = {'title': TextInput({'class': 'textinput form-control',
                                          'placeholder': 'Введите заголовок'}),
                   'anouncement': TextInput({'class': 'textinput form-control',
                                       'placeholder': 'Введите аннотацию'}),
                   'text': TextInput({'class': 'textinput form-control',
                                       'placeholder': 'Введите текст'}),
                   'image_field': FileInput({'class': 'form-control'}),
                   'tags': CheckboxSelectMultiple(),
                   }
