from django.contrib import admin

from .models import Group, Post


class PostAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group'
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    list_editable = ('group', 'text')


admin.site.register(Post, PostAdmin)
admin.site.register(Group)
