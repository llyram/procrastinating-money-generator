# models.py
from django.db import models

class TelegramUser(models.Model):
    user_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.username} (ID: {self.user_id})"
