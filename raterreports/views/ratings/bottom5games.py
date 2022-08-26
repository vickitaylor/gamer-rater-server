"""Module for generating bottom 5 games report"""
""" URL for this report is http://localhost:8000/reports/bottom_5_games """

from django.shortcuts import render
from django.db import connection
from django.views import View
from raterreports.views.helpers import dict_fetch_all

class Bottom5GamesList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # 🦕🦕🦕SQL query goes here🦜🦜🦜 
            db_cursor.execute("""
                SELECT 
                    g.id, 
                    g.title,
                    AVG(r.rating) AS AvgRating
                FROM raterapp_game g
                JOIN raterapp_rating r ON r.game_id = g.id
                GROUP BY r.game_id
                ORDER BY AvgRating
                LIMIT 5
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            bottom_five = []

            for row in dataset:
                # TODO: Create a dictionary 
                game = {
                    "id": row['id'],
                    "title": row["title"],
                    "Avg_Rating": row["AvgRating"]
                }

                bottom_five.append(game)

        # The template string must match the file name of the html template
        template = 'ratings/bottom_5_games.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "game_list": bottom_five
        }

        return render(request, template, context)
