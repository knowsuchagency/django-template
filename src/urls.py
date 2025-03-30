"""
URL configuration for django_template_test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

from core import views
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin/queue-monitor/", views.queue_monitor, name="admin_queue_monitor"),
    path("api/", api.urls),
    path("accounts/", include("allauth.urls")),
    path("_allauth/", include("allauth.headless.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]

urlpatterns += views.route.patterns
urlpatterns += debug_toolbar_urls()
