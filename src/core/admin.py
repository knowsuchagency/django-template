from django.contrib import admin
from django.urls import path

from .models import User, StockTicker
from .views import queue_monitor


# Register our models with the default admin site
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


# We need to patch the admin site to add our own custom urls and app list without
# replacing the existing admin site and third party apps registered with it.
original_get_urls = admin.site.get_urls
original_get_app_list = admin.site.get_app_list


# Customize the get_urls method
def custom_get_urls():
    urls = original_get_urls()
    custom_urls = [
        path(
            "queue-monitor/", admin.site.admin_view(queue_monitor), name="queue_monitor"
        ),
    ]
    return custom_urls + urls


# Customize the get_app_list method
def custom_get_app_list(request, app_label=None):
    app_list = original_get_app_list(request, app_label)

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


# Patch the existing admin site instead of replacing it
admin.site.get_urls = custom_get_urls
admin.site.get_app_list = custom_get_app_list
