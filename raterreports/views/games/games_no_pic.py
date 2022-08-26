"""Module for generating top 5 games report"""
""" URL for this report is http://localhost:8000/reports/no_pic """

from django.shortcuts import render
from django.db import connection
from django.views import View
from raterreports.views.helpers import dict_fetch_all

class GamesNoPic(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # 🦕🦕🦕SQL query goes here🦜🦜🦜 
            db_cursor.execute("""
                WITH NoPic AS (
                    SELECT 
                        g.id,
                        g.title,
                        COUNT(p.id) AS num
                    FROM raterapp_game g
                    LEFT JOIN raterapp_picture p ON p.game_id = g.id
                    GROUP BY g.id
                    )

                SELECT 
                    COUNT(*) AS zero
                FROM NoPic
                WHERE num = 0
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            no_pic = []

            for row in dataset:
                # TODO: Create a dictionary 
                game = {
                    "no_pic": row['zero']
                }

                no_pic.append(game)

        # The template string must match the file name of the html template
        template = 'games/games_no_pic.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "game_list": no_pic
        }

        return render(request, template, context)
