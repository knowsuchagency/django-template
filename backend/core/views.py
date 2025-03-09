from djecorator import Route
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

route = Route()


@route("/")
def landing(request):
    return render(request, "core/landing.html")


@route("/dashboard/")
@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")
