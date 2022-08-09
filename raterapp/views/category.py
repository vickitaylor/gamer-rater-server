from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from raterapp.models import Category


class CategoryView(ViewSet):
    """ Gamer Rater Category View
    """

    def list(self, request):
        """Handles the get request for the categories

        Returns:
            Response: JSON serialized list of categories
        """
        categories = Category.objects.all()

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    """

    class Meta:
        model = Category
        fields = ('id', 'name')
