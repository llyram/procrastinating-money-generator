# models.py
from django.db import models

class Reel(models.Model):
    reel_id = models.CharField(max_length=255)
    # Add more fields as needed

