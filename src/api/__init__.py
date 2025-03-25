from django.conf import settings
from ninja import NinjaAPI
from ninja.security import django_auth

from .v1.router import router as v1_router


def simple_auth(request):
    """
    This is exists so we can use our app within Lovable's preview environment.

    Make sure to add the request's actual unique origin i.e. `https://id-preview--d9666ffa-29be-443f-9013-25d5cd5c1beb.lovable.app` to `CSRF_TRUSTED_ORIGINS`.
    """
    return request.user and request.user.is_authenticated


api = NinjaAPI(
    auth=simple_auth if settings.DEBUG else django_auth,
)

api.add_router("/v1", v1_router)
