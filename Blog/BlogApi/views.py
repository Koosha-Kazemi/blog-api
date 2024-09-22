from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import serializers

from .permitions import *
from .models import Posts, Comments, Likes
from .serializer import PostSerializer, PostDetailSerializer, CreateCommentSerializer, LikeSerializer, \
CommentSerializer, AcceptCommentSerializer


class PostListCerate(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsWriterOrAdminOrReadOnly,)



class PostDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (IsWriterOrAdminOrReadOnly,)


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        elif self.request.method in ['PUT', 'PATCH']:
            return PostSerializer

    def get_object(self):
        return get_object_or_404(Posts, id=self.kwargs['pk'])



class CreateComment(generics.CreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CreateCommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        post = get_object_or_404(Posts, id = self.kwargs['pk'])
        serializer.save(post = post)




class CreateLike(generics.CreateAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        comment = get_object_or_404(Comments, id =self.kwargs['comment_id'])
        serializer.save(comment=comment)


class ResetLike(generics.UpdateAPIView):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(Likes, comment__id=self.kwargs['comment_id'])

    def perform_update(self, serializer):
        CurrentLikeStatus = self.request.data.get('is_like', 'false')
        like_status = self.get_object()
        if CurrentLikeStatus == like_status.is_like:
            like_status.delete()
        else :
            like_status.is_like = not like_status.is_like
            like_status.save()




class ReplyComment(generics.ListCreateAPIView):
    queryset = Comments.objects.all()


    def get_queryset(self):
        if self.request.method == 'GET':
            comment = get_object_or_404(Comments, id=self.kwargs['comment_id'])
            return comment.reply_user.filter(is_accept=True)
        elif self.request.method == "POST":
            return Comments.objects.all()

    def get_serializer_class(self):
            if self.request.method == "GET":
                return CommentSerializer
            elif self.request.method == "POST":
                return CreateCommentSerializer

    def perform_create(self, serializer):
        parent_comment = get_object_or_404(Comments, id=self.kwargs['comment_id'])
        if not parent_comment.reply_to:
            serializer.save(
                user = self.request.user,
                post = parent_comment.post,
                reply_to = parent_comment
            )
        else:
            raise serializers.ValidationError('you can not reply for reply comment')
        



class ReplyList(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        comment = get_object_or_404(Comments, id=self.kwargs['comment_id'])
        return comment.reply_user.all()



class CommentList(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAdmin,)

    def get_queryset(self):
        post = get_object_or_404(Posts, id=self.kwargs['pk'])
        return post.comment_post.filter(is_accept=False)




class AcceptComment(generics.UpdateAPIView):
    serializer_class = AcceptCommentSerializer
    permission_class = (IsAdmin,)

    def get_object(self):
            return get_object_or_404(Comments, id=self.kwargs['comment_id'])



class CommentReplyList(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_class = (IsAdmin,)
    def get_queryset(self):
        comment = get_object_or_404(Comments, id=self.kwargs['comment_id'])
        return comment.reply_user.filter(is_accept=False)