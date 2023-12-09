from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import datetime
from django.db.models import Count

class Tag(models.Model):
    title = models.CharField(max_length=80)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.title

    # def tag_count(self):
    #     count = self.article_set.count()
    #     # комментарий: когда мы работаем со связанными объектами (foreign_key, m2m, один к одному),
    #     # мы можем обращаться к связанным таблицам при помощи синтаксиса:
    #     # связаннаяМодель_set и что-то делать с результатами. В этом примере - мы используем связанные article
    #     # и вызываем метод count
    #     return count
    class Meta:
        ordering = ['title','status']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class PublishedToday(models.Manager):
    def get_queryset(self):
        return super(PublishedToday,self).get_queryset().filter(date__gte=datetime.date.today())

class Article(models.Model):
    categories = (('A', 'Животные'),
                  ('P', 'Растения'),
                  ('M', 'Микромир'),
                  ('W', 'Вода'),
                  ('N', 'Природа'))
    #поля                                       #models.CASCADE SET_DEFAULT (совсем удалить пользователя вместе с новостями)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField('Название', max_length=50, default='') #указывать длину обязательно#
    anouncement = models.TextField('Аннотация', max_length=250) #можно не указывать длину#
    text = models.TextField('Текст новости')
    date = models.DateTimeField('Дата публикации', auto_now=True) # auto_now=True - автоизменение новости auto_create=True - автосоздание новости#
    category = models.CharField(choices=categories, max_length=20, verbose_name='Категории')
    tags = models.ManyToManyField(to=Tag, blank=True)
    status = models.BooleanField(default=True)
    objects = models.Manager()
    published = PublishedToday()
    # image = models.ImageField(default='default1.jpg', null=True, blank=True, upload_to='images/')
    # slug = models.SlugField()
    # default='default1.jpg' - добавить в скобки полей для кари=тинок, если надо по умолчанию сделать дефолтную картинку

    #методы моделей
    def __str__(self):
        return f'{self.title} от: {str(self.date)[:16]}'
    def image_tag(self):
        image = Image.objects.filter(article=self)
        if image:
            return mark_safe('<img src="{}" height="50"/>'.format(image[0].image.url))
        else:
            return '(нет картинки)'

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

class Image(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(default='default1.jpg', null=True, upload_to='images/') #лучше добавить поле default !!!

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image is not None:
            return mark_safe(f'<img src="{self.image.url}" height="50px" width="auto" />')
        else:
            return '(нет картинки)'