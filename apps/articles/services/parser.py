import logging
from typing import List

import requests
from lxml import etree
from lxml.html import Element
from marshmallow import ValidationError

from apps.articles.dto.article import ArticleSchema, ArticleDto
from apps.articles.models.article import ArticleRepo


class ParserService:
    IDS_XPATH = "//tr[@class='athing']"
    LINKS_XPATH = "//a[@class='storylink']"
    LINK_KEY = "href"
    ID_KEY = "id"

    def __init__(self, base_url: str, path: str):
        self.base_url = base_url
        self.path = path

    def execute(self):
        """
        Parsing received html document
        Parsing table with posts contains rows with unique id which contains <a> tag with required data.
        In that case we can get ids and other info separately,
        cuz the received data will still keep its' order such as
        id list :   [1, 2, 3]
                     👇 👇 👇
        post list:  [1, 2, 3]
        """
        resp = requests.get(f"{self.base_url}/{self.path}")
        resp.raise_for_status()
        try:
            root = etree.HTML(resp.text)
            id_list = root.xpath(self.IDS_XPATH)
            link_list = root.xpath(self.LINKS_XPATH)
            articles = self._validate_articles(id_list=id_list, link_list=link_list)
            self._create_articles(articles=articles)
        except ValueError as e:
            logging.error(f"Value Error: {e.args}")
        except Exception as e:
            logging.exception(f"Unhandled error: {e.args}")

    @classmethod
    def _validate_articles(
        cls, id_list: List[Element], link_list: List[Element]
    ) -> List[ArticleDto]:
        """
        Method for validating received posts, schema checks
        for typing and presence of all of the required parameters.
        Checking for duplicates in received data.
        This method does not check existing records in DB.
        :param id_list: Received ids from html document
        :param link_list: Received links and titles from html document
        :return: Validated data that can be saved
        """
        result = []
        used_ids = []
        if not id_list or not link_list:
            raise ValueError("Empty article lists received, probably wrong keys for elements")

        if len(id_list) != len(link_list):
            raise ValueError("Parsed lists do not match, data structure has been changed")

        for idx in range(len(id_list)):
            try:
                if id_list[idx].get("id") in used_ids:
                    raise ValidationError(f"Duplicate id received: {id_list[idx].get('id')}")

                result.append(
                    ArticleSchema().load(
                        {
                            "id": id_list[idx].get("id"),
                            "url": link_list[idx].get("href"),
                            "title": link_list[idx].text,
                        }
                    )
                )
                used_ids.append(id_list[idx].get("id"))

            except ValidationError as e:
                logging.error(f"Error during post validation: {e.args}")

        return result

    @staticmethod
    def _create_articles(articles: List[ArticleDto]):
        """
        Method for creating articles from parsed posts.
        Checks the existing articles by checking post ids.
        :param articles: List of parsed articles
        :return:
        """
        if articles:
            existing = ArticleRepo.get_existing_objects(
                id_list=[article.id for article in articles]
            )
            articles = [article for article in articles if article.id not in existing]
            ArticleRepo.create_articles(articles=articles)
