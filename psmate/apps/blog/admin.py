from django.contrib import admin
from psmate.models import News

class BlogAdmin(admin.ModelAdmin):

    class Media:
        js = (
            '/static/tinymce/classictinymc.js',
            '/static/tinymce/tinymce.min.js',
        )

    prepopulated_fields = {'slug': ('title',)}


admin.site.register(News, BlogAdmin)

