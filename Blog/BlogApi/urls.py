from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from django.urls import path

from .views import *

urlpatterns = [
    path('posts/', PostView.as_view(), name = 'post_list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('posts/<int:pk>/comment/', CreateComment.as_view(), name='comment_create'),
    path('posts/<int:pk>/comment/<int:comment_id>/like/', CreateLike.as_view(), name='comment_like'),
    path('posts/<int:pk>/comment/<int:comment_id>/reset-like/', ResetLike.as_view(), name='reset_like'),
    path('comment/<int:comment_id>/reply/',CreateReply.as_view(), name='reply_create'),
    path('comment/<int:comment_id>/reply-view/', ReplyList.as_view(), name='reply_list'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

