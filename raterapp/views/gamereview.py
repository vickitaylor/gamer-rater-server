from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from raterapp.models import Review


class ReviewView(ViewSet):
    """Gamer Rater Review View
    """

    def list(self, request):
        """Handles the GET request for all reviews in the database

        Returns:
            Response: JSON serialized list of games
        """

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
            serializer = ReviewSerializer


class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for reviews
    """
    class Meta:
        model = Review
        fields = ('id', 'game_id', 'player_id')
        depth = 2
