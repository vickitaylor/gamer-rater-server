from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from raterapp.models import Rating, Player, Game


class RatingView(ViewSet):
    """ Gamer Rater Rating View
    """

    def list(self, request):
        """Handles the get request for the rating

        Returns:
            Response: JSON serialized list of rating
        """
        game_param = self.request.query_params.get('gameId', None)
        if game_param is not None:
            ratings = Rating.objects.filter(game_id=game_param)

        else:
            ratings = Rating.objects.all()

        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """ Handles the GET request for a single rating. If not found 404 returned.

        Returns:
            response: JSON serialized rating fo the selected key
        """
        try:
            rating = Rating.objects.get(pk=pk)
            serializer = RatingSerializer(rating)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Rating.DoesNotExist as ex:
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

        rating = Rating.objects.create(
            rating=request.data["rating"],
            player=player,
            game=game
        )

        serializer = RatingSerializer(rating)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a rating

        Returns:
            Response: Empty body with 204 status code
        """

        # getting the rating object requested by the primary key
        rating = Rating.objects.get(pk=pk)
        # setting fields on rating to the values coming in from the client
        rating.rating = request.data["rating"]

        # saving to the database
        rating.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class RatingSerializer(serializers.ModelSerializer):
    """JSON serializer for rating
    """

    class Meta:
        model = Rating
        fields = ('id', 'rating', 'game', 'player')
