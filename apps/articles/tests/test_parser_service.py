import logging
from unittest.mock import Mock

import pytest
import requests
from pytest_mock import MockFixture
from requests import Response

from apps.articles.models import Article
from apps.articles.services.parser import ParserService
from apps.articles.tests.fixtures.articles import ARTICLES_LIST


class MockElement:
    def __init__(self, data: dict):
        self.data = data
        self.text = data.get("text")

    def get(self, key):
        return self.data.get(key)


@pytest.mark.parametrize(
    "links, ids, valid, expected",
    (
        (
            [
                MockElement({ParserService.LINK_KEY: f"url{1}", "text": "text1"})
                for i in range(101, 115)
            ],
            [MockElement({ParserService.ID_KEY: i}) for i in range(101, 115)],
            True,
            len(list(range(101, 115))),
        ),
        (
            [
                MockElement({ParserService.LINK_KEY: f"url{1}", "text": "text1"})
                for i in range(10, 15)
            ],
            [MockElement({ParserService.ID_KEY: i}) for i in range(1, 15)],
            False,
            0,
        ),
        (
            [
                MockElement({ParserService.LINK_KEY: f"url1", "text": "text1"}),
                MockElement({ParserService.LINK_KEY: f"url2", "text": "text2"}),
            ],
            [MockElement({ParserService.ID_KEY: 21}), MockElement({ParserService.ID_KEY: 21})],
            True,
            1,
        ),
    ),
)
def test_parser(db, mocker: MockFixture, caplog, links, ids, valid, expected):
    caplog.set_level(logging.ERROR)
    mock_resp = Response()
    mock_resp.status_code = 200

    class MockHtml:
        @classmethod
        def xpath(cls, key):
            data = {ParserService.IDS_XPATH: ids, ParserService.LINKS_XPATH: links}
            return data.get(key)

    mocker.patch.object(requests, "get", return_value=mock_resp)
    mocker.patch("lxml.etree.HTML", Mock(return_value=MockHtml()))
    ParserService("", "").execute()
    assert Article.objects.all().count() == len(ARTICLES_LIST) + expected

    if not valid:
        assert "Value Error" in caplog.text
