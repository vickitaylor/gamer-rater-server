from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    designer = models.CharField(max_length=50)
    year_released = models.PositiveIntegerField(default=0)
    number_of_players = models.PositiveIntegerField(default=0)
    est_time_to_play = models.PositiveIntegerField(default=0)
    rec_age = models.PositiveSmallIntegerField(default=0)
    player = models.ForeignKey("Player", on_delete=models.CASCADE, related_name="player")
    categories = models.ManyToManyField("Category", through="GameCategories", related_name="games")
