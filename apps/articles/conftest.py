import pytest

from apps.articles.models import Article
from apps.articles.tests.fixtures.articles import ARTICLES_LIST


@pytest.fixture(autouse=True)
def fill_articles(db, django_db_setup):
    Article.objects.bulk_create((Article(**article.asdict()) for article in ARTICLES_LIST))
