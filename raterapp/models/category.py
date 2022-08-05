from django.db import models

from raterapp.models import game_categories

class Category(models.Model):
    name = models.CharField(max_length=50)
