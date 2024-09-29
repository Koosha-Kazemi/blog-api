from rest_framework import generics
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

from Account.serializer import RegisterUserSerializer


User = get_user_model()

class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)
            return Response({
               'refresh_token' : refresh_token,
                'access_token' : access_token
            })