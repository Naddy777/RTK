from django.contrib import admin
from .models import *
from django.db.models.functions import Length
from django.db.models import Count

class ArticleAdmin(admin.ModelAdmin):
    ordering = ['-date', 'author','title']
    list_display = ['title', 'author', 'date','category','image','image_tag', 'symbols_count']
    list_filter = ['title','author','date']
    list_display_links = ['date'] # список ссылок (нажимаешь - переходишь)
    readonly_fields = ['author'] # список полей, которые нельзя редактировать
    list_editable = ['title'] # список редактируемых полей
    # prepopulated_fields = {"slug":("title")} # добавление слага в админку
    list_per_page = 10 # пагинация (дление по стр)


    @admin.display(description='Длина', ordering='_symbols')
    def symbols_count(self, article: Article):
        return f"Символы: {len(article.text)}"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_symbols=Length('text'))
        return queryset
    #чтобы не поломать установленную сортировку
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'tag_count']
    list_filter = ['title', 'status']

    @admin.display(description='Использований', ordering='tag_count')
    def tag_count(self, object):
        return object.tag_count
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(tag_count=Count('article'))
        return queryset
#
 #
# admin.site.register(Tag,TagAdmin)
admin.site.register(Article, ArticleAdmin)