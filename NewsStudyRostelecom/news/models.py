from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Article(models.Model):
    categories = (('E','Economics')
                  ('S','Shince')
                  ('I','IT')


    )
    #поля                                       #models.CASCADE SET DEFAULT (совсем удалить пользователя вместе с новостями)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField('Название',max_length=50,default='')
    anouncement = models.TextField('Аннотация', max_length=250)
    text = models.TextField('Текст новости')
    data = models.DateTimeField('Дата публикации', auto_now=True)
    category = models.CharField(choices=categories,max_length=20,verbose_name='Категории')

    def __str__(self):
        return f' {self.title} от: {str(self.date})[:16]}'

    def get_absolute_url(self):
        return f'/news{self.id}'

    #метаданные модели
    class Meta:
        ordering = ['date','title']
        verbose_name ='Новости'
        verbose_name_plural ='Новости'
