from django.urls import path

from apps.articles import views

urlpatterns = [
    path("posts", views.ArticleView.as_view(), name="article_view"),
]
