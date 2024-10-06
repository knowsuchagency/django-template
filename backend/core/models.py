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
