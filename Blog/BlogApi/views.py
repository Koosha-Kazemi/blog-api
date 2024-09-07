from keyword import kwlist

from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Posts, Comments, Likes
from .serializer import PostSerializer, PostDetailSerializer, CreateCommentSerializer, LikeSerializer


class PostView(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveAPIView):
    serializer_class = PostDetailSerializer

    def get_object(self):
        return get_object_or_404(Posts, id=self.kwargs['pk'])

class CreateComment(generics.CreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CreateCommentSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Posts, id = self.kwargs['pk'])
        serializer.save(post = post)


class CreateLike(generics.CreateAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        comment = get_object_or_404(Comments, id =self.kwargs['comment_id'])
        serializer.save(comment=comment)


