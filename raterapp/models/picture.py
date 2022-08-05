from django.db import models

class Picture(models.Model):
    player = models.ForeignKey("Player", on_delete=models.CASCADE, related_name="picture_player")
    picture_url = models.URLField()
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="picture_game")
