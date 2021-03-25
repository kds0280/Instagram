from rest_framework import serializers
from post.models import Post, Comment
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_image']


class CommentListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'body', 'parent']


class CommentDetailSerializer(serializers.ModelSerializer):
    children = CommentListSerializer(many=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'body', 'children']


class PostListCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    comments = CommentListSerializer(many=True, source='get_two_comments')
    number_of_like = serializers.IntegerField(source='count_like')

    class Meta:
        model = Post
        fields = ['user', 'id', 'created_at', 'body', 'image', 'comments']
        extra_kwargs = {
            'body': {'write_only': True},
            'comments': {'read_only': True},
        }


class PostUpdateDeleteSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    comment = CommentDetailSerializer(many=True, source='get_all_comments')
    number_of_like = serializers.IntegerField(source='count_like')

    class Meta:
        model = Post
        fields = ['user', 'body', 'created_at', 'image', 'comment']
        extra_kwargs = {
            'image': {'read_only': True}
        }
