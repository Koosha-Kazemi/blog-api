from rest_framework import generics

from .models import Posts
from .serializer import PostSerializer


class PostList(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
