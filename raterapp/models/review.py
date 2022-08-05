from django.db import models

class Review(models.Model):
    player = models.ForeignKey("Player", on_delete=models.CASCADE, related_name="review_player")
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="review_game")
    review = models.CharField(max_length=300)
