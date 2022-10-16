from django.contrib import admin
from .models import Article

# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("source_name", "title", "pub_date")

