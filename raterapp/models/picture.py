from django.db import models


class Picture(models.Model):
    game = models.ForeignKey(
        "Game", on_delete=models.DO_NOTHING, related_name='pictures')
    action_pic = models.ImageField(
        upload_to='actionimages', height_field=None,
        width_field=None, max_length=None, null=True)
