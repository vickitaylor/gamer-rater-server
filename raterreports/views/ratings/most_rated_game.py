"""Module for generating top 5 games report"""
""" URL for this report is http://localhost:8000/reports/most_rated """

from django.shortcuts import render
from django.db import connection
from django.views import View
from raterreports.views.helpers import dict_fetch_all

class MostRatedGameList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # 🦕🦕🦕SQL query goes here🦜🦜🦜 
            db_cursor.execute("""
            SELECT 
                g.id, 
                g.title,
                COUNT(r.id) AS TimesRated
            FROM raterapp_game g
            JOIN raterapp_rating r ON r.game_id = g.id
            GROUP BY r.game_id
            ORDER BY TimesRated DESC
            LIMIT 1
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            most_rated = []

            for row in dataset:
                # TODO: Create a dictionary
                game = {
                    "id": row['id'],
                    "title": row["title"],
                    "TimesRated": row["TimesRated"]
                }

                most_rated.append(game)

        # The template string must match the file name of the html template
        template = 'ratings/most_rated_game.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "game_list": most_rated
        }

        return render(request, template, context)
