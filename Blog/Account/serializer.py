from rest_framework.serializers import ModelSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )