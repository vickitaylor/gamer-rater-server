"""Module for generating top 5 games report"""
""" URL for this report is http://localhost:8000/reports/most_games """

from django.shortcuts import render
from django.db import connection
from django.views import View
from raterreports.views.helpers import dict_fetch_all

class PlayerMostGames(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # 🦕🦕🦕SQL query goes here🦜🦜🦜 
            db_cursor.execute("""
                WITH Most AS (
                    SELECT
                        u.id,
                        u.first_name|| ' ' || u.last_name AS Name,
                        COUNT(g.player_id) AS GamesFromPlayer
                    FROM raterapp_game g
                    JOIN raterapp_player p ON p.id = g.player_id
                    JOIN auth_user u ON u.id = p.user_id
                    GROUP BY player_id
                    )

                SELECT 
                    Name
                FROM Most
                WHERE GamesFromPlayer = (
                    SELECT
                        MAX(GamesFromPlayer)
                    FROM Most
                )
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            most_games = []

            for row in dataset:
                # TODO: Create a dictionary 
                game = {
                    "name": row['Name']
                }

                most_games.append(game)

        # The template string must match the file name of the html template
        template = 'games/player_most_games.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "game_list": most_games
        }

        return render(request, template, context)
