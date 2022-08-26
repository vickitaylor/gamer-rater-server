from django.urls import path

from .views import (Top5GamesList, Bottom5GamesList,
                    MostRatedGameList, TopReviewers, GamesByCategory, MoreThan5Players,
                    PlayerMostGames, Under8)

urlpatterns = [
    path('reports/top_5_games', Top5GamesList.as_view()),
    path('reports/bottom_5_games', Bottom5GamesList.as_view()),
    path('reports/most_rated', MostRatedGameList.as_view()),
    path('reports/top_reviewers', TopReviewers.as_view()),
    path('reports/games_by_category', GamesByCategory.as_view()),
    path('reports/morethan5', MoreThan5Players.as_view()),
    path('reports/most_games', PlayerMostGames.as_view()),
    path('reports/under8', Under8.as_view())
]
