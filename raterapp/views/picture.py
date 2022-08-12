import uuid
import base64
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.files.base import ContentFile

from raterapp.models import Game, Picture


class PictureView(ViewSet):
    """GamerRater Photo View
    """

    def list(self, request):
        """Handles the get request for the game photos for the selected game
        """
        game_param = self.request.query_params.get('gameId', None)
        if game_param is not None:
            pictures = Picture.objects.filter(game_id=game_param)
        else:
            pictures = Picture.objects.all()

        serializer = PictureSerializer(pictures, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """POST for user to upload picture
        """
        # create a new instance of the game picture model that was defined
        # ex= game_picture = GamePicture()


        format, imgstr = request.data["game_image"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr),
                           name=f'{request.data["game_id"]}-{uuid.uuid4()}.{ext}')

        # give the image property of your game picture instance a value
        # ex if named "action pic", then you would use
        #           game_picture.action_pic = data
        # save using save() method

        picture = Picture.objects.create(
            game_id=request.data['game_id'],
            action_pic=data
        )
        serializer = PictureSerializer(picture)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PictureSerializer(serializers.ModelSerializer):
    """JSON serializer for rating
    """
    class Meta:
        model = Picture
        fields = ('id', 'game', 'action_pic')
