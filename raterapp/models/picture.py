from django.db import models

class Picture(models.Model):
    player = models.ForeignKey("Player", on_delete=models.CASCADE, related_name="picture_player")
    picture_url = models.CharField(max_length=300)
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="picture_game")
