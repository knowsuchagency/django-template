import json
import pprint
import re
from typing import Any, List
from urllib.parse import urlparse

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.middleware.csrf import CsrfViewMiddleware


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


class WildcardCSRFMiddleware(CsrfViewMiddleware):
    """
    Extends Django's CSRF middleware to support wildcard patterns in CSRF_TRUSTED_ORIGINS.

    This allows configurations like:
        CSRF_TRUSTED_ORIGINS = ['https://*.knowsuchagency.com']

    Which will match any subdomain of knowsuchagency.com.
    """

    def _get_trusted_origins(self) -> List[str]:
        """
        Return the list of trusted origins, some of which may contain wildcards.
        """
        return getattr(settings, "CSRF_TRUSTED_ORIGINS", [])

    def _process_wildcard_patterns(self, request_origin: str) -> bool:
        """
        Check if the request origin matches any of our wildcard patterns in CSRF_TRUSTED_ORIGINS.

        For example, if CSRF_TRUSTED_ORIGINS contains 'https://*.knowsuchagency.com',
        and the request origin is 'https://subdomain.knowsuchagency.com', this should match.
        """
        trusted_origins = self._get_trusted_origins()

        for trusted_origin in trusted_origins:
            # Skip if this isn't a wildcard pattern
            if "*" not in trusted_origin:
                continue

            # Convert the wildcard pattern to a regex pattern
            # First, escape all special regex characters
            pattern = re.escape(trusted_origin)

            # Then replace the escaped wildcard with a regex pattern for any subdomain
            # The pattern "[^.]+\." matches any sequence of characters that aren't dots,
            # followed by a dot, which is exactly what we want for a subdomain
            pattern = pattern.replace("\\*", "[^.]+")

            # Add start and end anchors
            pattern = f"^{pattern}$"

            # Check if the request origin matches our pattern
            if re.match(pattern, request_origin):
                return True

        return False

    def process_view(self, request, callback, callback_args, callback_kwargs):
        """
        Override the process_view method to check for wildcard matches before
        falling back to the standard CSRF validation.
        """
        # Skip CSRF checks for CSRF exempt views
        if getattr(callback, "csrf_exempt", False):
            return None

        # Get the request origin
        request_origin = request.META.get("HTTP_ORIGIN")

        # If there's an origin header and it matches one of our wildcard patterns,
        # temporarily allow this request
        if request_origin and self._process_wildcard_patterns(request_origin):
            # Mark this request as having passed CSRF validation
            request.META["_dont_enforce_csrf_checks"] = True
            return None

        # Otherwise, use the standard CSRF validation
        return super().process_view(request, callback, callback_args, callback_kwargs)
