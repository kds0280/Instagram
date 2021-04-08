from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from base_api import CreateAPIViewWithoutSerializer, UpdateAPIViewWithoutSerializer
from post.models import Post, Comment
from post.permissions import IsObjectMineOrReadOnly
from post.serializers import PostListCreateSerializer, PostUpdateDeleteSerializer, CommentListSerializer


class PostListCreate(generics.ListAPIView, CreateAPIViewWithoutSerializer):
    queryset = Post.objects.all()
    serializer_class = PostListCreateSerializer
    schema = {'body': {'type': 'string'},
              'image': {'type': 'file', 'nullable': False}}
    class_to_create_object = Post
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def create_instance(self, request, **isvalid_data):
        return self.class_to_create_object.objects.create(**isvalid_data, user=request.user)


class PostDetailUpdateDelete(generics.RetrieveDestroyAPIView, UpdateAPIViewWithoutSerializer):
    schema = {'body': {'type': 'string'},
              'image': {'type': 'file', 'nullable': False}}
    lookup_field = 'id'
    lookup_url_kwarg = 'post_id'
    queryset = Post.objects.all()
    serializer_class = PostUpdateDeleteSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsObjectMineOrReadOnly,
    )


class CommentCreate(CreateAPIViewWithoutSerializer):
    serializer_class = CommentListSerializer
    schema = {'post_id': {'type': 'integer', 'excludes': 'parent_id', 'required': True},
              'parent_id': {'type': 'integer', 'excludes': 'post_id', 'required': True},
              'body': {'type': 'string', 'empty': False}}
    class_to_create_object = Comment

    def create_instance(self, request, **isvalid_data):
        if 'parent_id' in isvalid_data:
            isvalid_data['post_id'] = Comment.objects.get(id=isvalid_data['parent_id']).post_id
        return self.class_to_create_object.objects.create(**isvalid_data, user=request.user)


class CommentDelete(generics.DestroyAPIView):
    serializer_class = CommentListSerializer
    queryset = Comment.objects.all()
    lookup_url_kwarg = 'comment_id'
    lookup_field = 'id'
    permission_classes = (
        IsObjectMineOrReadOnly,
    )


class PostLike(generics.GenericAPIView):
    permission_classes = (
        IsAuthenticated,
    )

    def patch(self, request, *args, **kwargs):
        if Post.objects.filter(id=kwargs['post_id'], like_users=request.user.id).exists():
            request.user.like_posts.remove(kwargs['post_id'])
            result = {'result': False}
            return Response(result)
        else:
            request.user.like_posts.add(kwargs['post_id'])
            result = {'result': True}
            return Response(result)
