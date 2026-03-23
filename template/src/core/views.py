from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required


def root_redirect(request):
    """Redirect root to app"""
    return redirect("/app/")


def index(request):
    """Serve the React SPA"""
    return render(request, "index.html")


def spa_fallback(request, path):
    """Fallback for client-side routing"""
    return render(request, "index.html")


@staff_member_required
def task_monitor(request):
    """Combined Task Monitor view with workflow monitoring and conductor"""
    return render(request, "admin/task_monitor.html")
