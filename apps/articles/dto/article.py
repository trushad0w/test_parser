from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from marshmallow import Schema, fields, post_load

from core.dto import BaseDto


@dataclass
class ArticleDto(BaseDto):
    id: int
    url: str
    title: str
    created: datetime = None


class ArticleSchema(Schema):
    id = fields.Int(required=True)
    url = fields.Str(required=True)
    title = fields.Str(required=True)

    @post_load
    def make_model(self, data, **kwargs):
        return ArticleDto.make(data)


class OrderEnum(str, Enum):
    ID = "id"
    URL = "url"
    TITLE = "title"

    def __str__(self):
        return self.value


class OrderDirectionEnum(str, Enum):
    ASC = "asc"
    DESC = "desc"

    def __str__(self):
        return self.value

    @classmethod
    def get_direction(cls, value: str):
        if value == cls.ASC:
            return ""
        return "-"
