from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def set_csrf_token(request):
    return JsonResponse({"details": "CSRF cookie set"})


def landing_page(request):
    return render(request, "core/landing.html")


@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")
