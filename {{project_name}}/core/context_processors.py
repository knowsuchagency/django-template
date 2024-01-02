from django.conf import settings


def debug_context(request):
    return {"DEBUG": settings.DEBUG}
