"""Module for generating top 5 games report"""
""" URL for this report is http://localhost:8000/reports/top_reviewers """

from django.shortcuts import render
from django.db import connection
from django.views import View
from raterreports.views.helpers import dict_fetch_all

class TopReviewers(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # 🦕🦕🦕SQL query goes here🦜🦜🦜 
            db_cursor.execute("""
            SELECT 
                u.id,
                u.first_name|| ' ' || u.last_name AS Name,
                COUNT(r.id) AS TimesReviewed
            FROM raterapp_review r 
            JOIN raterapp_player p ON p.id = r.player_id
            JOIN auth_user u ON u.id = p.user_id
            GROUP BY r.player_id
            ORDER BY TimesReviewed DESC
            LIMIT 3
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            top_reviewers = []

            for row in dataset:
                # TODO: Create a dictionary 
                reviewer = {
                    "id": row["id"],
                    "Name": row["Name"],
                    "TimesReviewed": row["TimesReviewed"]
                }

                top_reviewers.append(reviewer)

        # The template string must match the file name of the html template
        template = 'reviews/top_reviewers.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "reviewer_list": top_reviewers
        }

        return render(request, template, context)
