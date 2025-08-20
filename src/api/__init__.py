from django.conf import settings
from ninja import NinjaAPI
from ninja.security import APIKeyHeader, SessionAuthIsStaff

from .v1.router import router as v1_router


class ApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        if key == settings.X_API_KEY:
            return key


api = NinjaAPI(
    auth=[ApiKey(), SessionAuthIsStaff()],
)

api.add_router("/v1", v1_router)
