from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class Genres(models.Model):
    name = models.CharField(max_length = 12)

    def __str__(self):
        return self.name


class Posts(models.Model):
    title = models.CharField(max_length = 15)
    text = models.TextField(max_length = 500)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    publish = models.DateTimeField(auto_now_add = True)
    update = models.DateTimeField(auto_now = True)
    genre = models.ManyToManyField(Genres)

    def __str__(self):
        return f'{self.title} by {self.author.username}'



