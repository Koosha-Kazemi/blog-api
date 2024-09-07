from django.urls import path

from .views import *

urlpatterns = [
    path('posts/', PostView.as_view(), name = 'post_list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('posts/<int:pk>/comment/', CreateComment.as_view(), name='comment_create'),
    path('posts/<int:pk>comment/<int:pk>/like', CreateLike.as_view(), name = 'comment_like'),

    
]

