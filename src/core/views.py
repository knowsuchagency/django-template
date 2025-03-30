from django.http import HttpResponse
from djecorator import Route
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

route = Route()


@route("/")
def landing(request):
    return render(request, "core/landing.html")


@route("/dashboard/", login_required=True)
def dashboard(request):
    return render(request, "core/dashboard.html")


@staff_member_required
def queue_monitor(request):
    """Queue monitoring view for the admin interface"""
    context = {
        "title": "Queue Monitor",  # This will be shown in the admin title
    }
    return render(request, "admin/queue_monitor.html", context)
