from django.conf import settings


def debug_context(request):
    return {"DEBUG": settings.DEBUG}


def dev_context(request):
    return {"DEV": settings.STAGE == "DEV"}
