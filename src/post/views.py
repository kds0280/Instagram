from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from my_validator import check_validation
from post.base_api import CreateAPIViewWithoutSerializer
from post.models import Post, Comment
from post.permissions import IsObjectMineOrReadOnly
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

    def create_instance(self, request, **isvalid_data):
        return self.class_to_create_object.objects.create(**isvalid_data, user=request.user)


class PostDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
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
    schema = {'post_id': {'type': 'string', 'regex': '^[0-9]+$'},
              'parent_id': {'type': 'string', 'regex': '^[0-9]+$', 'empty': True},
              'body': {'type': 'string', 'empty': False}}
    class_to_create_object = Comment

    def create_instance(self, request, **isvalid_data):
        if isvalid_data['parent_id']:
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
        IsAuthenticatedOrReadOnly,
    )

    def patch(self, request, *args, **kwargs):
        if Post.objects.filter(id=kwargs['post_id'], like_users=request.user.id).first():
            request.user.like_posts.remove(kwargs['post_id'])
            return Response(False)
        else:
            request.user.like_posts.add(kwargs['post_id'])
            return Response(True)
