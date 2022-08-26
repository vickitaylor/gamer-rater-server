from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from raterapp.models import Rating, Player
from raterapp.views.rating import RatingSerializer


class RatingTest(APITestCase):

    # fixtures to run to build the database
    fixtures = ['users', 'tokens', 'players',
                'categories', 'games', 'ratings']

    def setUp(self):
        # getting the first player object from the database and adding their tokens to the headers
        self.player = Player.objects.first()
        token = Token.objects.get(user=self.player.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_rating(self):
        """ Test the create rating method
        """
        url = "/ratings"

        # defining the rating properties
        rating = {
            "rating": 8,
            "game": 1
        }

        response = self.client.post(url, rating, format='json')

        # the expected output comes first, the actual is second.
        # the expected status code is 201, the actual status code received
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        # gets the last game added to database
        new_rating = Rating.objects.last()

        # since the create method should return the serialized version of the new rating,
        # use the serializer using in the create method to serialize the rating
        expected = RatingSerializer(new_rating)

        # testing the expected output matches the actual
        self.assertEqual(expected.data, response.data)

    def test_update_rating(self):
        """test update rating method"""

        # getting the first rating in the database
        rating = Rating.objects.first()

        url = f'/ratings/{rating.id}'

        updated_rating = {
            "rating": 7
        }
        response = self.client.put(url, updated_rating, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Refresh the game object to reflect any changes to the database
        rating.refresh_from_db()

        # assert that the updated value matches
        self.assertEqual(updated_rating['rating'], rating.rating)
