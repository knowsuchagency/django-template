from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def landing_page(request):
    return render(request, "core/landing.html")


@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")
