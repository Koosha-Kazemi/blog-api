from django.urls import path

from .views import *

urlpatterns = [
    path('posts/', PostList.as_view(), name = 'post_list'),
    
]

