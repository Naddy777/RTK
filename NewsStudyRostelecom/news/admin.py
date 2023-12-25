from django.contrib import admin
from .models import *
from django.db.models.functions import Length
from django.db.models import Count

class ArticleFilter(admin.SimpleListFilter):
    title = 'По длине новости'
    parameter_name = 'text'

    def lookups(self, request, model_admin):
        return [('S',("Короткие, <500 зн.")),
                ('M',("Средние, 500-1000 зн.")),
                ('L',("Длинные, >1000 зн.")),]

    def queryset(self, request, queryset):
        if self.value() == 'S':
            return queryset.annotate(text_len=Length('text')).filter(text_len__lt=500)
        elif self.value() == 'M':
            return queryset.annotate(text_len=Length('text')).filter(text_len__lt=1000,
                                                                     text_len__gte=500)
        elif self.value() == 'L':
            return queryset.annotate(text_len=Length('text')).filter(text_len__gt=1000)

class ArticleImageInline(admin.TabularInline): # есть еще StackedInline - другое расположение полей
    model = Image
    extra = 3
    readonly_fields = ('id','image_tag')

class ArticleAdmin(admin.ModelAdmin):
    ordering = ['-date', 'author','title']
    list_display = ['title', 'author', 'date','status','category','image_tag', 'symbols_count']
    list_filter = [ArticleFilter,'author','date', 'status']
    list_display_links = ['date'] # список ссылок (нажимаешь - переходишь)
    search_fields = ['title__icontains','tags__title'] #поиск по связанному полю теги по заголовку,
    readonly_fields = ['author'] # список полей, которые нельзя редактировать
    list_editable = ['title'] # список редактируемых полей
    filter_horizontal = ['tags'] # список полей для М2М
    # prepopulated_fields = {"slug":("title")} # добавление слага в админку
    list_per_page = 10 # пагинация (дление по стр)
    inlines = [ArticleImageInline]
    actions = ['set_true', 'set_false']


    @admin.display(description='Длина', ordering='_symbols')
    def symbols_count(self, article: Article):
        return f"Символы: {len(article.text)}"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_symbols=Length('text'))
        return queryset
    #чтобы не поломать установленную сортировку

    @admin.action(description='Активировать выбранные новости')
    def set_true(self, request, queryset):
        amount = queryset.update(status=True)
        self.message_user(request, f'Активировано {amount} статей')

    @admin.action(description='Деактивировать выбранные новости')
    def set_false(self, request, queryset):
        amount = queryset.update(status=False)
        self.message_user(request, f'Деактивировано {amount} статей')
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'tag_count']
    list_filter = ['title', 'status']
    actions = ['set_true', 'set_false']

    @admin.display(description='Использований', ordering='tag_count')
    def tag_count(self, object):
        return object.tag_count
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(tag_count=Count('article'))
        return queryset
    @admin.action(description='Активировать выбранные теги')
    def set_true(self, request, queryset):
        amount = queryset.update(status=True)
        self.message_user(request, f'Активировано {amount} тегов')

    @admin.action(description='Деактивировать выбранные теги')
    def set_false(self, request, queryset):
        amount = queryset.update(status=False)
        self.message_user(request, f'Деактивировано {amount} тегов')
 #
# admin.site.register(Tag,TagAdmin)
admin.site.register(Article, ArticleAdmin)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title','article','image_tag']

@admin.register(ViewCount)
class ViewCountAdmin(admin.ModelAdmin):
    list_display = ['article','ip_address','view_date']