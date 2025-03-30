from django.contrib import admin
from django.urls import path
from django.utils.html import format_html

from .models import User, StockTicker
from .views import queue_monitor


# Store reference to the original method
original_get_urls = admin.AdminSite.get_urls


# Fix the get_urls implementation
def get_urls(self):
    # Call the original method, not our own implementation
    urls = original_get_urls(self)
    custom_urls = [
        path("queue-monitor/", self.admin_view(queue_monitor), name="queue_monitor"),
    ]
    return custom_urls + urls


# Monkey patch the AdminSite.get_urls with our custom method
admin.AdminSite.get_urls = get_urls


# Store reference to the original app list method
original_get_app_list = admin.AdminSite.get_app_list


# Add a custom method to the admin site to get our custom app list
def get_app_list(self, request, app_label=None):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.
    """
    app_list = original_get_app_list(self, request, app_label)

    # Add our Queue Monitor to the app list
    app_dict = {
        "name": "Queue Management",
        "app_label": "queue_management",
        "app_url": "#",
        "has_module_perms": True,
        "models": [
            {
                "name": "Queue Monitor",
                "object_name": "queue_monitor",
                "perms": {"add": False, "change": False, "delete": False, "view": True},
                "admin_url": "/admin/queue-monitor/",
                "view_only": True,
            }
        ],
    }

    # Insert at the beginning for visibility
    app_list.insert(0, app_dict)

    return app_list


# Monkey patch the AdminSite.get_app_list with our custom method
admin.AdminSite.get_app_list = get_app_list


# Register our models
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    ]


@admin.register(StockTicker)
class StockTickerAdmin(admin.ModelAdmin):
    list_display = [
        "symbol",
        "company_name",
        "price",
        "change",
        "percent_change",
        "volume",
        "date",
    ]
    list_filter = ["date", "symbol"]
    search_fields = ["symbol", "company_name"]
