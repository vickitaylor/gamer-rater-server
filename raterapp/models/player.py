from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    """ the player model, inherits properties form the parent class models.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    bio = models.CharField(max_length=300)
