from django.contrib import admin

from apps.articles.models import Article


@admin.register(Article)
class AdminArticle(admin.ModelAdmin):
    change_list_template = "article_changelist.html"
    list_display = ["id", "title", "url", "created"]
