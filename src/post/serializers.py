from rest_framework import serializers
from post.models import Post, Comment
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_image']


class PostListCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ['user_id', 'id', 'created_at', 'like_count', 'body']
        extra_kwargs = {
            'body': {'write_only': True}
        }


class PostUpdateDeleteSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Post
        fields = ['user', 'body', 'created_at', 'like_count', 'image', 'comment']
        extra_kwargs = {
            'like_count': {'read_only': True},
            'image': {'read_only': True}
        }
