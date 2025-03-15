import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    class Meta:
        db_table = "user"

    # the uuid is what we'll use in the unsubscribe link
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    groups = models.ManyToManyField(Group, related_name="accounts_user_groups")
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="accounts_user_permissions",
    )


class StockTicker(models.Model):
    class Meta:
        db_table = "stock_ticker"
        ordering = ["-date", "symbol"]

    symbol = models.CharField(max_length=10)
    company_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    change = models.DecimalField(max_digits=10, decimal_places=2)
    percent_change = models.DecimalField(max_digits=5, decimal_places=2)
    volume = models.BigIntegerField()
    market_cap = models.BigIntegerField(null=True, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.symbol} - {self.date} - ${self.price}"
