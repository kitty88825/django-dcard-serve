from django.db import models

from apps.users.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    managers = models.ManyToManyField(User, related_name="manage_categories")
    subscribers = models.ManyToManyField(
        User,
        related_name="subscribe_categories",
    )
