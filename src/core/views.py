from djecorator import Route
from django.shortcuts import render

route = Route()


@route("/")
def landing(request):
    return render(request, "core/landing.html")


@route("/dashboard/", login_required=True)
def dashboard(request):
    return render(request, "core/dashboard.html")
