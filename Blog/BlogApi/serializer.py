from rest_framework import serializers

from django.contrib.auth import get_user_model

from django.contrib.auth.models import AnonymousUser

from .models import Genres, Posts, Comments, Likes

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name',)



class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ('is_like',)


    def create(self, validated_data):
            request = self.context['request']
            validated_data['user'] = request.user
            return Likes.objects.create(**validated_data)

    def update(self, instance, validated_data):
            instance.is_like = validated_data('is_like', instance.is_like)
            instance.save()
            return instance



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

         if isinstance(user, AnonymousUser):
             raise serializers.ValidationError('you cant post')

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
    like = serializers.SerializerMethodField()
    dislike = serializers.SerializerMethodField()
    class Meta:
        model = Comments
        exclude = ('is_accept','reply_to')

    def get_like(self, obj):
        return Likes.objects.filter(comment=obj, is_like=True).count()

    def get_dislike(self, obj):
        return Likes.objects.filter(comment=obj, is_like=False).count()


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
    comment = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Posts
        fields = '__all__'


    def get_comment(self, obj):
        comment = Comments.objects.filter(post=obj, is_accept=True, reply_to__isnull=True)
        return CommentSerializer(comment, many=True).data



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.username
        representation['genre'] = ', '.join([genre.name for genre in instance.genre.all()])
        return representation





class AcceptCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('is_accept',)

    def update(self, instance, validated_data):
            instance.is_accept= validated_data.get('is_accept', instance.is_accept)
            instance.save()
            return instance

