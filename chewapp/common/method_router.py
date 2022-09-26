from typing import Dict, Any
from collections.abc import Callable
from django.http import HttpRequest, HttpResponse

Handler = Callable[[HttpRequest], HttpResponse]


def route(method_map: Dict[str, Handler], *args, **kwargs):
    def handler(request: HttpRequest, *args, **kwargs):
        if request.method in method_map:
            return method_map[request.method](request, *args, **kwargs)

    return handler
