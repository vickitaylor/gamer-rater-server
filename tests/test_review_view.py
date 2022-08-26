from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from raterapp.models import Review, Player
from raterapp.views.gamereview import ReviewSerializer


class ReviewTest(APITestCase):

    # fixtures to run to build the database
    fixtures = ['users', 'tokens', 'players',
                'categories', 'games', 'reviews']

    def setUp(self):
        # getting the first player object from the database and adding their tokens to the headers
        self.player = Player.objects.first()
        token = Token.objects.get(user=self.player.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_review(self):
        """ Test the create review method
        """
        url = "/reviews"

        # defining the review properties
        review = {
            "game": 1,
            "review": "Great game!"
        }

        response = self.client.post(url, review, format='json')

        # the expected output comes first, the actual is second.
        # the expected status code is 201, the actual status code received
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        # gets the last review added to database
        new_review = Review.objects.last()

        # since the create method should return the serialized version of the new review,
        # use the serializer using in the create method to serialize the review
        expected = ReviewSerializer(new_review)

        # testing the expected output matches the actual
        self.assertEqual(expected.data, response.data)

    def test_update_review(self):
        """test update review method"""

        # getting the first review in the database
        review = Review.objects.first()

        url = f'/reviews/{review.id}'

        updated_review = {
            "review": f'{review.review} updated'
        }

        response = self.client.put(url, updated_review, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Refresh the review object to reflect any changes to the database
        review.refresh_from_db()

        # assert that the updated value matches
        self.assertEqual(updated_review['review'], review.review)
