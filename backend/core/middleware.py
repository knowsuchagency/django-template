import pprint
import re
from typing import List, Set
from urllib.parse import urlparse

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.middleware.csrf import CsrfViewMiddleware
import logging

logger = logging.getLogger(__name__)


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


class DynamicCookieDomainsMiddleware:
    """
    Middleware that dynamically sets cookie domains for CSRF and session cookies
    based on the request origin and CSRF_TRUSTED_ORIGINS.

    This allows cookies to be shared across backend and frontend domains without
    requiring explicit configuration of CSRF_COOKIE_DOMAIN and SESSION_COOKIE_DOMAIN.

    Features:
    - Support for wildcard patterns in CSRF_TRUSTED_ORIGINS
    - Dynamic discovery of appropriate cookie domains
    - Support for preview deployments at arbitrary URLs
    - Works across separate backend and frontend domains

    Instead of using a single cookie domain, this middleware sets the appropriate
    domain for each cookie based on the request's origin and the trusted origins.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self._extract_base_domains()
        self._log_domains()

    def _extract_base_domains(self) -> None:
        """
        Extract base domains from CSRF_TRUSTED_ORIGINS.
        Converts patterns like 'https://*.example.com' to '.example.com'.
        """
        self.base_domains = set()

        for origin in getattr(settings, "CSRF_TRUSTED_ORIGINS", []):
            parsed_url = urlparse(origin)
            domain = parsed_url.netloc

            # Handle wildcard domains
            if domain.startswith("*."):
                # Convert *.example.com to .example.com (Django's cookie domain format)
                domain = domain[1:]  # Remove the *
            elif "." in domain and not domain.startswith("."):
                # For non-wildcard domains like example.com, prepend with dot
                # to make it work with subdomains (.example.com)
                domain = f".{domain}"

            # Skip localhost/IP address domains as they shouldn't have a leading dot
            if domain in ("localhost", "127.0.0.1") or re.match(
                r"\d+\.\d+\.\d+\.\d+", domain
            ):
                continue

            # Extract port if present
            if ":" in domain:
                domain = domain.split(":")[0]

            if domain and len(domain) > 1:  # Ensure we have a meaningful domain
                self.base_domains.add(domain)

    def _log_domains(self) -> None:
        """Log the extracted cookie domains."""
        if self.base_domains:
            logger.info(f"Extracted cookie domains: {sorted(self.base_domains)}")
        else:
            logger.warning(
                "No cookie domains extracted from CSRF_TRUSTED_ORIGINS. "
                "This may cause CSRF validation issues across different domains."
            )

    def _get_request_domain(self, request: HttpRequest) -> str:
        """
        Get the domain from the request's origin or host header.

        Returns:
            The domain from the request, or None if it couldn't be determined.
        """
        # First try to get it from the Origin header
        origin = request.META.get("HTTP_ORIGIN")
        if origin:
            parsed_url = urlparse(origin)
            return parsed_url.netloc

        # Fall back to the Host header
        return request.get_host().split(":")[0]

    def _find_matching_cookie_domain(self, request_domain: str) -> str:
        """
        Find the most specific cookie domain that matches the request domain.

        For example, if request_domain is 'app.example.com', and self.base_domains
        contains ['.example.com', '.app.com'], it will return '.example.com'.

        Returns:
            The matching cookie domain, or None if no match is found.
        """
        # For localhost/IPs, use exact domain (no leading dot)
        if request_domain in ("localhost", "127.0.0.1") or re.match(
            r"\d+\.\d+\.\d+\.\d+", request_domain
        ):
            return request_domain

        # Find all matching domains
        matching_domains = []
        for domain in self.base_domains:
            # Check if the request domain ends with the cookie domain
            # (e.g., app.example.com ends with .example.com)
            if domain.startswith(".") and request_domain.endswith(domain[1:]):
                matching_domains.append(domain)

        # Return the most specific (longest) match
        if matching_domains:
            return max(matching_domains, key=len)

        # If no match found and not localhost/IP, try with a leading dot
        if "." in request_domain and not request_domain.startswith("."):
            return f".{request_domain}"

        # Last resort - use the domain as is
        return request_domain

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process the request, set appropriate cookie domains, and pass it to the next middleware.
        """
        response = self.get_response(request)

        # Only modify cookies if we have base domains extracted
        if not self.base_domains:
            return response

        # Get the domain from the request
        request_domain = self._get_request_domain(request)
        if not request_domain:
            return response

        # Find the matching cookie domain
        cookie_domain = self._find_matching_cookie_domain(request_domain)

        # Set cookie domain for any cookies present in the response
        cookies_to_modify = ["csrftoken", "sessionid"]
        for cookie_name in cookies_to_modify:
            if cookie_name in response.cookies:
                cookie = response.cookies[cookie_name]
                # Only set domain if not already set or if it's different
                if not cookie.get("domain") or cookie.get("domain") != cookie_domain:
                    cookie["domain"] = cookie_domain
                    if settings.DEBUG:
                        logger.debug(
                            f"Set {cookie_name} cookie domain to {cookie_domain}"
                        )

        return response
