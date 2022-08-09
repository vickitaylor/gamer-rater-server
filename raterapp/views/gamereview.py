from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from raterapp.models import Review, Player, Game


class GameReviewView(ViewSet):
    """Gamer Rater Review View
    """

    def list(self, request):
        """Handles the GET request for all reviews in the database.
        Has an if function to see if there is a query parameter. The query parameter is to
        filter is to get all reviews per the gameId. url .../reviews?gameId=x, if true, all
        reviews for the game are stored, if None, than there is no query and the full list returns

        Returns:
            Response: JSON serialized list of games
        """
        # defining the query parameter for the request
        game_param = self.request.query_params.get('gameId', None)
        if game_param is not None:
            # defined variable to store the objects that match the query
            reviews = Review.objects.filter(game_id=game_param)

        else:
            reviews = Review.objects.all()

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """ Handles the GET request for a single review. If not found 404 returned.

        Returns:
            response: JSON serialized review fo the selected key
        """
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handles the POST operation

        Returns:
            Response: JSON serialized game instance
        """
        # getting the logged in user id
        player = Player.objects.get(user=request.auth.user)
        # getting the game pk
        game = Game.objects.get(pk=request.data["game"])

        review = Review.objects.create(
            review=request.data["review"],
            player=player,
            game=game
        )

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# created a user serializer, to only return certain fields from the user model


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users, to have only the id, username, and name fields return
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')

# created the player serializer and used the user serializer to include the users info that was
# selected in the US above, so that fields not needed are not brought in.


class PlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for player date received
    """
    # assigned the data from the UserSerializer to the user variable
    user = UserSerializer()

    class Meta:
        model = Player
        # selected the fields to return in the player object, the user data returns as an
        # object in player
        fields = ('id', 'bio', 'user')


class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for reviews
    """

    player = PlayerSerializer()

    class Meta:
        model = Review
        fields = ('id', 'review', 'game', 'player')
