from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class AccountAdmin(admin.ModelAdmin):
    list_display = ['user','gender']
    list_filter = ['user','gender']

admin.site.register(Account,AccountAdmin)


def make_author(modeladmin,request,queryset):
    group = Group.objects.get(name='Author')
    ungroup = Group.objects.get(name='Actions_Required')
    for user in queryset:
        user.groups.add(group)
        user.groups.remove(ungroup)

make_author.short_description = "Утвердить автора"


class CustomUserAdmin(UserAdmin):
    actions = [make_author]
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class FavoriteArticleAdmin(admin.ModelAdmin):
    list_display = ['article','user','create_at']
admin.site.register(FavoriteArticle, FavoriteArticleAdmin)