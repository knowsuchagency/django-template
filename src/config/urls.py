from django.contrib import admin
from django.urls import path, include
from core.views import queue_monitor

urlpatterns = [
    path("admin/", admin.site.urls),
    # Add your custom admin view
    path("admin/queue-monitor/", queue_monitor, name="admin_queue_monitor"),
    # ...other URL patterns
]
