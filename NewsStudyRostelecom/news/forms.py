from django import forms
from django.core.validators import MinLengthValidator
from .models import Article
from django.forms import ModelForm, Textarea, CheckboxSelectMultiple

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title','anouncement','text','image','tags','category']
        widgets = {
            'anouncement': Textarea(attrs={'cols':80,'rows':2}),
            'text': Textarea(attrs={'cols': 80, 'rows': 2}),
            'tags': CheckboxSelectMultiple(),
            # 'image': N ),
        }

