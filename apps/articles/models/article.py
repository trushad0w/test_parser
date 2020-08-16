from typing import List, Tuple

from django.db import models, connection

from apps.articles.dto.article import ArticleDto, OrderEnum, OrderDirectionEnum


class Article(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "article"


class ArticleRepo:
    DEFAULT_BATCH_SIZE = 100

    @staticmethod
    def get_existing_objects(id_list: List[int]):
        query = """
             select coalesce(array_agg(a.id), array[]::int[]) from unnest(%(id_list)s::int[]) id_list
                join article a on a.id=id_list 
        """
        with connection.cursor() as cursor:
            cursor.execute(sql=query, params={"id_list": id_list})
            return cursor.fetchone()[0]

    @classmethod
    def create_articles(cls, articles: List[ArticleDto]):
        Article.objects.bulk_create(
            (Article(**article.asdict()) for article in articles),
            batch_size=cls.DEFAULT_BATCH_SIZE,
        )

    @staticmethod
    def get_articles(
        order: OrderEnum, order_direction: OrderDirectionEnum, limit: int, offset: int
    ) -> Tuple[int, List[ArticleDto]]:
        articles = Article.objects.all().order_by(
            f"{OrderDirectionEnum.get_direction(order_direction)}{order}"
        )
        return (
            articles.count(),
            [ArticleDto.make(article.__dict__) for article in articles[offset : offset + limit]],
        )
