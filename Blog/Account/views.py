from rest_framework import generics

from Account.serializer import RegisterUserSerializer

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer


    def perform_create(self, serializer):
        password = make_password(self.request.data.get('password'))
        serializer.save(
            password = password
        )




