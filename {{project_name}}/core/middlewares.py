from urllib.parse import urlsplit
from django.conf import settings


def htmx_redirect_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        if request.headers.get("HX-Request") and response.status_code == 302:
            location = urlsplit(response["Location"])
            if location.path == settings.LOGIN_URL:
                redirect_url = (
                    f"{settings.LOGIN_URL}?next={settings.LOGIN_REDIRECT_URL}"
                )
                response["HX-Redirect"] = redirect_url
                response.status_code = 204
        return response

    return middleware
