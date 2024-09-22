from token import CIRCUMFLEX

from django.urls import path

from .views import *

urlpatterns = [
    path('posts/', PostListCerate.as_view(), name = 'post_ListCreate'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('posts/<int:pk>/comment/', CreateComment.as_view(), name='comment_create'),
    path('posts/<int:pk>/comment/list', CommentList.as_view(), name='comment_list'),
    path('comment/<int:comment_id>/accept/', AcceptComment.as_view(), name='accept_like'),
    path('comment/<int:comment_id>/like/', CreateLike.as_view(), name='comment_like'),
    path('comment/<int:comment_id>/reset-like/', ResetLike.as_view(), name='reset_like'),
    path('comment/<int:comment_id>/reply/', ReplyComment.as_view(), name='reply_create'),

]

