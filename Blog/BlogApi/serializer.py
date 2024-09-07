from dataclasses import replace

from rest_framework import serializers

from django.contrib.auth import get_user_model
from setuptools.config.pyprojecttoml import validate
from yaml import serialize_all

from .models import Genres, Posts, Comments, Likes

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name',)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields ='__all__'


class UserSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ('username',)



class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only = True)
    class Meta:
            model = Posts
            fields = '__all__'

    @staticmethod
    def get_author(obj):
         return obj.author.username


    def to_representation(self, instance):
         representation = super().to_representation(instance)
         representation['genre'] = [genre.name for genre in instance.genre.all()]
         return representation


    def create(self, validated_data):
         user = self.context['request'].user
         validated_data['author'] = user
         genre_data = validated_data.pop('genre')
         post = Posts.objects.create(**validated_data)
         post.genre.set(genre_data)
         return post
    

    def update(self,instance,validata_data):
         instance.title = validata_data.get('title',instance.title)
         instance.text = validata_data.get('text',instance.text)
         genre_data = validata_data.pop('genre')
         instance.genre.set(genre_data)
         instance.save()
         return instance




class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        exclude = ('is_accept',)

    def create(self, validated_data):
        request = self.context['request']
        post = request.data.get('post')
        user = request.user
        validated_data['post'] = post
        validated_data['user'] = user
        return Comments.objects.create(**validated_data)

    def update(self, instance, validate_data):
        instance.comment = validate_data.get('comment', instance.comment)
        instance.reply = validate_data.get('reply', instance.reply)
        instance.comment = validate_data.get('like_dislike', instance.like_dislike)
        instance.save()
        return instance


    def to_representation(self, instance):
            representation = super().to_representation(instance)
            representation['user'] = instance.user.username
            return representation


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('comment',)
        

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Comments.objects.create(**validated_data)



class PostDetailSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(source='comment_post', read_only=True, many=True)
    class Meta:
        model = Posts
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.username
        representation['genre'] = ', '.join([genre.name for genre in instance.genre.all()])
        return representation