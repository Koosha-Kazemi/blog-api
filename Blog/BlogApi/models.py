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



class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete = models.CASCADE, null=True, blank=True ,related_name = 'comment_post')
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField(max_length=100)
    is_accept = models.BooleanField(default = False)
    reply_to = models.ForeignKey('self', blank = True, null = True, on_delete = models.CASCADE, related_name='reply_user')
    create = models.DateTimeField(auto_now_add = True)
    update = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.user.username}'


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)
    is_like = models.BooleanField()