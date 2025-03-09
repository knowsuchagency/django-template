from django.contrib import admin

from .models import User, StockTicker


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
