from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    designer = models.CharField(max_length=50)
    year_released = models.PositiveIntegerField(default=0)
    number_of_players = models.PositiveIntegerField(default=0)
    est_time_to_play = models.PositiveIntegerField(default=0)
    rec_age = models.PositiveSmallIntegerField(default=0)
    player = models.ForeignKey(
        "Player", on_delete=models.CASCADE, related_name="player")
    categories = models.ManyToManyField(
        "Category", through="GameCategories", related_name="games")

    @property
    def average_rating(self):
        """Average rating calculated attribute for each game
        """
        ratings = self.ratings.all()

        # Sum all of the ratings for the game
        sum_rating = 0
        # looping thru the ratings to sum all ratings
        for rating in ratings:
            sum_rating += rating.rating

        # if statement since cannot divide by 0
        if sum_rating > 0:
            total_ratings = len(ratings)
            # getting the amount of ratings
            # getting the average
            average = sum_rating / total_ratings
            return average
        else:
            return "Game has not been rated.  Rate the game below!"
