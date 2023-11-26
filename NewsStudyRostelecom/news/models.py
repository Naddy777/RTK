from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class Tag(models.Model):
    title = models.CharField(max_length=80)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title','status']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

import datetime
class PublishedToday(models.Manager):
    def get_queryset(self):
        return super(PublishedToday,self).get_queryset().filter(date__gte=datetime.date.today())

class Article(models.Model):
    categories = (('A', 'Animals'),
                  ('P','Plants'),
                  ('M', 'Mickro'),
                  ('W', 'Water'),
                  ('N', 'Nature'))
    #поля                                       #models.CASCADE SET_DEFAULT (совсем удалить пользователя вместе с новостями)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField('Название',max_length=50, default='') #указывать длину обязательно#
    anouncement = models.TextField('Аннотация', max_length=250) #можно не указывать длину#
    text = models.TextField('Текст новости')
    date = models.DateTimeField('Дата публикации', auto_now=True) # auto_now=True - автоизменение новости auto_create=True - автосоздание новости#
    category = models.CharField(choices=categories, max_length=20, verbose_name='Категории')
    tags = models.ManyToManyField(to=Tag, blank=True)
    objects = models.Manager()
    published = PublishedToday()
    image = models.ImageField(blank=True, upload_to='images/')
    #методы моделей
    def __str__(self):
        return f'{self.title} от: {str(self.date)[:16]}'
    def image_tag(self):
        if self.image is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    #
    def get_absolute_url(self):
        return f'/news/{self.id}' # еще допускается ключ pk#
    #
    #метаданные модели
    class Meta:
        ordering = ['date','title']
        verbose_name ='Новость'
        verbose_name_plural ='Новости'
    #
    # def tag_list(self):
    #     s = ''
    #     for t in self.tags.all():
    #         s += t.title + ' '
    #     return s
