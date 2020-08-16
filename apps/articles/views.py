from urllib.parse import urlparse

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from marshmallow import Schema, fields, validate, EXCLUDE

from apps.articles.dto.article import OrderEnum, OrderDirectionEnum
from apps.articles.services.article import ArticleService
from apps.articles.tasks import fetch_new_articles
from core.api import api_call


class ArticleGetRequest(Schema):
    limit = fields.Int(validate=validate.Range(min=0, max=100), missing=5)
    offset = fields.Int(validate=validate.Range(min=0), missing=0)
    order = fields.Str(
        validate=validate.OneOf(tuple(OrderEnum.__members__.values())), missing=OrderEnum.ID
    )
    order_direction = fields.Str(
        validate=validate.OneOf(tuple(OrderDirectionEnum.__members__.values())),
        missing=OrderDirectionEnum.ASC,
    )

    class Meta:
        unknown = EXCLUDE


class ArticleView(View):
    @method_decorator(api_call(method="ArticleView->GET"), name="dispatch")
    def get(self, request: WSGIRequest):
        request_data = ArticleGetRequest().load(request.GET)
        total, data = ArticleService.get_articles(**request_data)

        return {
            "items": [article.asdict() for article in data],
            "limit": request_data["limit"],
            "offset": request_data["offset"],
            "total": total,
        }

    def post(self, request: WSGIRequest):
        if request.user.is_authenticated:
            fetch_new_articles.send()
            referrer_url = urlparse(request.META.get("HTTP_REFERER"))
            return HttpResponseRedirect(referrer_url.path)
        return HttpResponse("Not Authorized", status=403)
