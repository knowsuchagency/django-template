from django.test import TestCase, override_settings, Client
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.urls import path


# Test view that requires CSRF protection
@csrf_protect
@ensure_csrf_cookie  # This will ensure the CSRF cookie is set in the response
def test_csrf_view(request):
    return HttpResponse("CSRF check passed")


urlpatterns = [
    path("test-csrf/", test_csrf_view, name="test_csrf"),
]


@override_settings(ROOT_URLCONF=__name__)
class WildcardCSRFMiddlewareTests(TestCase):
    """Test the WildcardCSRFMiddleware with various origins."""

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    @override_settings(CSRF_TRUSTED_ORIGINS=["https://*.example.com"])
    def test_wildcard_domain_match(self):
        """Test that a request from a subdomain of a trusted wildcard origin is allowed."""
        # Get CSRF token first
        response = self.client.get("/test-csrf/")
        csrftoken = response.cookies["csrftoken"].value

        # Simulate a POST request from a subdomain
        response = self.client.post(
            "/test-csrf/",
            data={},
            HTTP_ORIGIN="https://subdomain.example.com",
            HTTP_REFERER="https://subdomain.example.com/some-page",
            headers={"X-CSRFToken": csrftoken},
        )
        self.assertEqual(response.status_code, 200)

    @override_settings(CSRF_TRUSTED_ORIGINS=["https://*.example.com"])
    def test_non_matching_domain(self):
        """Test that a request from an untrusted domain is blocked."""
        # Get CSRF token first
        response = self.client.get("/test-csrf/")
        csrftoken = response.cookies["csrftoken"].value

        # Simulate a POST request from an untrusted domain
        response = self.client.post(
            "/test-csrf/",
            data={},
            HTTP_ORIGIN="https://untrusted.com",
            HTTP_REFERER="https://untrusted.com/some-page",
            headers={"X-CSRFToken": csrftoken},
        )
        self.assertEqual(response.status_code, 403)  # Should be forbidden

    @override_settings(
        CSRF_TRUSTED_ORIGINS=["https://*.example.com", "http://localhost:8000"]
    )
    def test_mixed_trusted_origins(self):
        """Test that both wildcard and exact origins work together."""
        # Get CSRF token first
        response = self.client.get("/test-csrf/")
        csrftoken = response.cookies["csrftoken"].value

        # Simulate a POST request from localhost (exact match)
        response = self.client.post(
            "/test-csrf/",
            data={},
            HTTP_ORIGIN="http://localhost:8000",
            HTTP_REFERER="http://localhost:8000/some-page",
            headers={"X-CSRFToken": csrftoken},
        )
        self.assertEqual(response.status_code, 200)
