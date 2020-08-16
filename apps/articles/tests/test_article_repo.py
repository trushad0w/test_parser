import pytest

from apps.articles.dto.article import OrderDirectionEnum, OrderEnum
from apps.articles.models.article import ArticleRepo
from apps.articles.tests.fixtures.articles import ARTICLES_LIST


@pytest.mark.parametrize(
    "id_list, expected_size",
    (
        ([article.id for article in ARTICLES_LIST], len(ARTICLES_LIST)),
        ([ARTICLES_LIST[0].id], 1),
        ([], 0),
    ),
)
def test_get_existing_objects(db, id_list, expected_size):

    articles = ArticleRepo.get_existing_objects(id_list=id_list)
    assert (
        len(articles) == expected_size
    ), "Received existing articles does not match the expected result"
    article_ids = [article.id for article in ARTICLES_LIST]

    assert (
        len(set(articles) - set(article_ids)) == 0
    ), "Received existing articles does not exist in mock"


@pytest.mark.parametrize("limit", (0, 10, 100, 50))
@pytest.mark.parametrize("offset", (0, 1, 10))
@pytest.mark.parametrize("order", OrderEnum.__members__.values())
@pytest.mark.parametrize("order_direction", OrderDirectionEnum.__members__.values())
def test_get_articles(db, limit, offset, order, order_direction):
    count, _ = ArticleRepo.get_articles(
        order=order, order_direction=order_direction, limit=limit, offset=offset
    )

    assert count == offset or count == len(
        ARTICLES_LIST
    ), "Received empty articles, while offset is less than mocked articles count"
