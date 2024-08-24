from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class Genres(models.Model):
    name = models.CharField(max_length = 12)

    def __str__(self):
        return self.name

