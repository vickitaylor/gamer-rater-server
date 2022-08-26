from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from raterapp.models import Game, Player
from raterapp.views.game import GameSerializer


class GameTest(APITestCase):

    # fixtures to run to build the database
    fixtures = ['users', 'tokens', 'players',
                'categories', 'games']

    def setUp(self):
        # getting the first player object from the database and adding their tokens to the headers
        self.player = Player.objects.first()
        token = Token.objects.get(user=self.player.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_game(self):
        """ Test the create game method
        """
        url = "/games"

        # defining the game properties
        game = {
            "description": "its a game",
            "designer": "Milton Bradley",
            "est_time_to_play": 30,
            "number_of_players": 2,
            "rec_age": 5,
            "title": "Clue",
            "year_released": 1956,
            "category": 1
        }

        response = self.client.post(url, game, format='json')

        # the expected output comes first, the actual is second.
        # the expected status code is 201, the actual status code received
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        # gets the last game added to database
        new_game = Game.objects.last()

        # since the create method should return the serialized version of the new game,
        # use the serializer using in the create method to serialize the game
        expected = GameSerializer(new_game)

        # testing the expected output matches the actual
        self.assertEqual(expected.data, response.data)

    def test_get_game(self):
        """Testing the get single game method"""

        # getting a game from the database
        game = Game.objects.first()

        url = f'/games/{game.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # running thru the serializer
        expected = GameSerializer(game)

        # assert that the expected matches the actual received
        self.assertEqual(expected.data, response.data)

    def test_list_games(self):
        """Testing the get all game method"""

        url = '/games'

        response = self.client.get(url)

        # running thru the serializer, 🐶🐶🐶 have to have the object.xyz match the get on the view
        all_games = Game.objects.all().order_by("title")
        expected = GameSerializer(all_games, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_update_game(self):
        """test update game method"""

        # getting the first game in the database
        game = Game.objects.first()

        url = f'/games/{game.id}'

        updated_game = {
            "description": f'{game.description} updated',
            "designer": game.designer,
            "est_time_to_play": game.est_time_to_play,
            "number_of_players": game.number_of_players,
            "rec_age": game.rec_age,
            "title": game.title,
            "year_released": game.year_released,
            # 🦜🦜🦜 why did this category work ???🦜🦜🦜
            "category": 1
        }

        response = self.client.put(url, updated_game, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Refresh the game object to reflect any changes to the database
        game.refresh_from_db()

        # assert that the updated value matches
        self.assertEqual(updated_game['description'], game.description)

    def test_delete_game(self):
        """Testing the delete game method"""

        game = Game.objects.first()

        url = f'/games/{game.id}'

        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # testing to see if the deleted game returns with a get
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
