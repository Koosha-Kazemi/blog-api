from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Genres, Posts


User = get_user_model()




class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name',)




class UserSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ('username',)




class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only = True)
   

    class Meta:
            model = Posts
            fields = '__all__'


    def get_author(self,obj):
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
    


