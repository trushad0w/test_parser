import dramatiq

from apps.articles.services.parser import ParserService
from conf.settings import PARSER_BASE_URL, PARSER_PATH


@dramatiq.actor
def fetch_new_articles():
    ParserService(base_url=PARSER_BASE_URL, path=PARSER_PATH).execute()
