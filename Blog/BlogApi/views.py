from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Posts, Comments
from .serializer import PostSerializer, PostDetailSerializer, CreateCommentSerializer


class PostList(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer


class PostDetail(APIView):
    def get(self,request,*args,**kwargs):
        post = get_object_or_404(Posts, id = kwargs['pk'])
        serializer = PostDetailSerializer(post)
        return Response({
            'post' : serializer.data
        })


class CreateComment(generics.CreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CreateCommentSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Posts, id = self.kwargs['pk'])
        serializer.save(post = post)


