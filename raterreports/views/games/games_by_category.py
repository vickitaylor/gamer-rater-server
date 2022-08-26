"""Module for generating top 5 games report"""
""" URL for this report is http://localhost:8000/reports/games_by_category """

from django.shortcuts import render
from django.db import connection
from django.views import View
from raterreports.views.helpers import dict_fetch_all

class GamesByCategory(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # 🦕🦕🦕SQL query goes here🦜🦜🦜 
            db_cursor.execute("""
                SELECT 
                    c.id,
                    c.name,
                    COUNT(g.id) AS number
                FROM raterapp_game g
                JOIN raterapp_gamecategories gc ON gc.game_id = g.id
                JOIN raterapp_category c ON c.id = gc.category_id
                GROUP BY gc.category_id
                ORDER BY c.name
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            games_by_cat = []

            for row in dataset:
                # TODO: Create a dictionary 
                category = {
                    "id": row['id'],
                    "name": row["name"],
                    "number": row["number"]
                }

                games_by_cat.append(category)

        # The template string must match the file name of the html template
        template = 'games/games_by_category.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "cat_list": games_by_cat
        }

        return render(request, template, context)
