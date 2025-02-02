import json
import pprint
from typing import Any

from django.http import HttpRequest, HttpResponse


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Process request metadata before the view
        self._log_request(request)

        # Get response from view
        response = self.get_response(request)

        return response

    def _log_request(self, request: HttpRequest) -> None:
        """Pretty print request metadata including headers and cookies."""
        request_data = {
            "path": request.path,
            "method": request.method,
            "scheme": request.scheme,
            "get_params": dict(request.GET),
            "post_params": dict(request.POST),
            "headers": dict(request.headers),
            "cookies": dict(request.COOKIES),
            "user": str(request.user),
            "is_secure": request.is_secure(),
            "is_ajax": request.headers.get("X-Requested-With") == "XMLHttpRequest",
            "client_ip": request.META.get("REMOTE_ADDR"),
        }

        print("\n" + "=" * 50 + " REQUEST METADATA " + "=" * 50)
        pprint.pprint(request_data, indent=2, width=120)
        print("=" * 120 + "\n")
