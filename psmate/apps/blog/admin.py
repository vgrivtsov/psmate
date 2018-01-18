from django.contrib import admin
from psmate.models import News

class BlogAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}


admin.site.register(News, BlogAdmin)

