import functools
import logging

from django.http import JsonResponse
from marshmallow import ValidationError

from core.errors import BaseError


def api_call(*args, **kwargs):
    if kwargs:

        def wrapper(func):
            return ApiCall(func=func, **kwargs)

        return wrapper
    else:
        return ApiCall(*args)


class ApiCall(object):
    def __init__(self, func, method: str, status: int = 200):
        self.func = func
        self.method = method
        self.data = None
        self.status = status
        self.error_info = None
        functools.update_wrapper(self, func)

    def __process_exception(self, request, exception):
        logging.exception(exception)
        error_info = serialize_exception(exception)
        if isinstance(exception, BaseError):
            response_status = exception.status_code
        else:
            response_status = error_info["error"]["code"]
        self.error_info = error_info
        self.status = response_status

    def __call__(self, *args, **kwargs):
        request = args[0]
        try:
            return JsonResponse(data=self.func(*args, **kwargs))
        except Exception as e:
            self.__process_exception(request, e)
            return JsonResponse(self.error_info, status=self.status)


def serialize_exception(e: "Exception") -> dict:
    err_info = dict()
    err_info["message"] = getattr(e, "message", str(e))
    if not isinstance(e, BaseError) and not isinstance(e, ValidationError):
        err_info["message"] = f'Unhandled error: {err_info["message"]}'

    default_status_code = 500
    if isinstance(e, ValidationError):
        default_status_code = 400
    error_code = getattr(e, "status_code", default_status_code)

    error = {"error": {"code": error_code, "error": err_info}}

    return error
