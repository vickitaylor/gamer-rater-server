"""Module for generating top 5 games report"""
""" URL for this report is http://localhost:8000/reports/morethan5 """

from django.shortcuts import render
from django.db import connection
from django.views import View
from raterreports.views.helpers import dict_fetch_all

class MoreThan5Players(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # 🦕🦕🦕SQL query goes here🦜🦜🦜 
            db_cursor.execute("""
                SELECT 
                    g.id,
                    g.title,
                    g.number_of_players
                FROM raterapp_game g
                WHERE g.number_of_players > 5
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            more_than5 = []

            for row in dataset:
                # TODO: Create a dictionary 
                game = {
                    "id": row['id'],
                    "title": row["title"],
                    "number_of_players": row["number_of_players"]
                }

                more_than5.append(game)

        # The template string must match the file name of the html template
        template = 'games/morethan5players.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "game_list": more_than5
        }

        return render(request, template, context)
