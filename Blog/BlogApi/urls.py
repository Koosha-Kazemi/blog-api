from django.urls import path

from .views import *

urlpatterns = [
    path('posts/', PostList.as_view(), name = 'post_list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('posts/<int:pk>/comment/', CreateComment.as_view(), name='comment_create')

    
]

