from typing import List, Tuple

from apps.articles.dto.article import OrderEnum, OrderDirectionEnum, ArticleDto
from apps.articles.models.article import ArticleRepo


class ArticleService:
    @staticmethod
    def get_articles(
        order: OrderEnum, order_direction: OrderDirectionEnum, limit: int, offset: int
    ) -> Tuple[int, List[ArticleDto]]:
        return ArticleRepo.get_articles(
            order=order, order_direction=order_direction, limit=limit, offset=offset
        )
