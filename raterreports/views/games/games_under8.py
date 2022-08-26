"""Module for generating top 5 games report"""
""" URL for this report is http://localhost:8000/reports/most_games """

from django.shortcuts import render
from django.db import connection
from django.views import View
from raterreports.views.helpers import dict_fetch_all

class Under8(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # 🦕🦕🦕SQL query goes here🦜🦜🦜 
            db_cursor.execute("""
                SELECT 
                    g.id,
                    g.title,
                    g.rec_age
                FROM raterapp_game g
                WHERE g.rec_age < 8
                ORDER BY lower(g.title)
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            under8 = []

            for row in dataset:
                # TODO: Create a dictionary 
                game = {
                    "id": row['id'],
                    "title": row['title'],
                    "rec_age": row['rec_age']
                }

                under8.append(game)

        # The template string must match the file name of the html template
        template = 'games/games_under8.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "game_list": under8
        }

        return render(request, template, context)
