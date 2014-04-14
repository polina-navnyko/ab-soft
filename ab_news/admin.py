from django.contrib import admin
from models import Article


class NewsAdmin(admin.ModelAdmin):
    list_display = ['text', 'author', 'created', 'sent']
    search_fields = ['text']
    exclude = ['author', 'sent']
    ordering = ['-created']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


admin.site.register(Article, NewsAdmin)
