from djecorator import Route
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required

route = Route()


@route("/")
def root_redirect(request):
    """Redirect root to app"""
    return redirect("/app/")


@route("/app/")
def index(request):
    """Serve the React SPA"""
    return render(request, "index.html")


# Catch-all route for React Router - must be last
@route("/app/<path:path>")
def spa_fallback(request, path):
    """Fallback for client-side routing"""
    return render(request, "index.html")


@staff_member_required
def queue_monitor(request):
    """Queue monitoring view for the admin interface"""
    return render(request, "admin/queue_monitor.html")
