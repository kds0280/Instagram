from cerberus import Validator
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from post.base_api import CreateAPIViewWithoutSerializer
from post.models import Post, Comment
from post.permissions import IsPostMineOrReadOnly, IsCommentMineOrReadOnly
from post.serializers import PostListCreateSerializer, PostUpdateDeleteSerializer, CommentListSerializer


class PostListCreate(generics.ListAPIView, CreateAPIViewWithoutSerializer):
    queryset = Post.objects.all()
    serializer_class = PostListCreateSerializer
    schema = {'body': {'type': 'string'},
              'image': {'type': 'file'}}
    class_to_create_object = Post
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )


class PostDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'post_id'
    queryset = Post.objects.all()
    serializer_class = PostUpdateDeleteSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsPostMineOrReadOnly,
    )


class CommentCreate(CreateAPIViewWithoutSerializer):
    serializer_class = CommentListSerializer
    schema = {'post_id': {'regex': '^[0-9]+$'},
              'parent_id': {'regex': '^[0-9]+$', 'nullable': True},
              'body': {'type': 'string'}}
    class_to_create_object = Comment

    def check_validation(self, validator, **data):
        if data['parent_id']:
            data['post_id'] = Comment.objects.get(id=data['parent_id']).post_id
        super().check_validation(validator, **data)


class CommentDelete(generics.DestroyAPIView):
    serializer_class = CommentListSerializer
    queryset = Comment.objects.all()
    lookup_url_kwarg = 'comment_id'
    lookup_field = 'id'
    permission_classes = (
        IsCommentMineOrReadOnly,
    )
