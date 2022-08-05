from django.db import models

class Rating(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="rating_game")
    player = models.ForeignKey("Player", on_delete=models.CASCADE, related_name="rating_player")
    rating = models.IntegerField(default=0)
