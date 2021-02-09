from rest_framework import serializers
from post.models import Post


class PostListCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ['user_id', 'id', 'created_at', 'like_count', 'body']
        extra_kwargs = {
            'body': {'write_only': True}
        }


class PostUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user_id', 'body', 'created_at', 'like_count']
        extra_kwargs = {
            'like_count': {'read_only': True}
        }
