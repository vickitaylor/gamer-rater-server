from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from raterapp.models import Game, Player, Category


class GameView(ViewSet):
    """Gamer Rater Games View

    Args:
        ViewSet (class): It is a class that combines related views. It is a type of class-based
        View, that does not provide any method handlers such as .get() or .post(), it instead
        provides actions such as .list() and .create().
    """

    def list(self, request):
        """ Handles the GET request for all games in the database

        Returns:
            Response: JSON serialized list of games
        """
        # new variable games, gets a list of all the game objects returned to it, sorted by title
        games = Game.objects.all().order_by("title")

        # then the data from games is passed to the serializer and stored in serializer, many=True
        # is added so that is knows it is a list
        serializer = GameSerializer(games, many=True)
        # then the data stored in serializer is returned in JSON format
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """ Handles the GET request for a single game. If one is not found, it will return 404.

        Args:
            request (dict): the query parameter for the request
            pk (int): primary key of the game being requested.

        Returns:
            response: JSON serializer game gor the selected key
            events = Event.objects.filter(organizer__user=request.auth.user)
        """
        # game = Game.objects.filter(player__user=request.auth.user)
        try:
            # matching the received primary key to the list of games primary keys
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """ Handles the POST operation

        Args:
            request (dict): The object that is being created.

        Returns:
            Response: JSON serialized game instance
        """
        # variable that stores gets and stores the logged in user
        player = Player.objects.get(user=request.auth.user)

        # game variable declared, and the parameters of the fields, are being passed to the create
        # method.
        game = Game.objects.create(
            description=request.data["description"],
            designer=request.data["designer"],
            est_time_to_play=request.data["est_time_to_play"],
            number_of_players=request.data["number_of_players"],
            rec_age=request.data["rec_age"],
            title=request.data["title"],
            year_released=request.data["year_released"],
            player=player
        )
        # for the (*request) it is needed to add for a list (ie in postman, if category:[1, 2, 3])
        # you need the *, if just sending 1 like when using select in react, you dont use the *
        # as it is not receiving a list
        game.categories.add(request.data["category"])
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """ Handles PUT requests for the game, only the maker can edit.

        Returns:
            Response: Empty body with a 204 status code.
        """
        # getting the game by its primary key
        game = Game.objects.get(pk=pk)
        # setting the fields to the values coming in
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.est_time_to_play = request.data["est_time_to_play"]
        game.number_of_players = request.data["number_of_players"]
        game.rec_age = request.data["rec_age"]
        game.title = request.data["title"]
        game.year_released = request.data["year_released"]

        # saving selections
        game.save()
        # assuming since the categories are many to many, that they have to be cleared out
        # prior to saving again
        game.categories.clear()
        # then resaves the category selected.
        game.categories.add(request.data["category"])

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handles the delete request for a game
        """
        # finding the game from the pk received
        game = Game.objects.get(pk=pk)

        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Args:
        serializers (class): the serializer class which gives you a powerful, generic way to
        control the output of your responses.  ModelSerializer class which provides a useful
        shortcut for creating serializers that deal with model instances and querysets.
    """
    class Meta:
        """Meta is the inner class of the model class, it is used to change the behavior
        of your model fields.
        For average_rating, could not access rating to show as a field, but since average_rating
        is on the game model, was able to access that property.
        Added try/except due to receipt of ZeroDivisionError, if there is an average rating
        the field will be returned, if the game has not yet been rated then the expect model
        will kick in and not return the avg rating field
        """

        try:
            model = Game
            fields = ('id', 'title', 'designer', 'description', 'year_released',
                      'number_of_players', 'est_time_to_play', 'rec_age', 'categories',
                      'player', 'average_rating')
            depth = 1
        except ZeroDivisionError as ex:
            model = Game
            fields = ('id', 'title', 'designer', 'description', 'year_released',
                      'number_of_players', 'est_time_to_play', 'rec_age', 'categories', 'player')
            depth = 1
