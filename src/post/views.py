"""
API 클래스를 2개 만들기
 - Post List API (Serializer)
    - user_id
    - created_at
    - like_counts
 - Post Create API
    - user_id
    - body
    - 생성 후 Detail 과 동일한 리턴
 - Post Detail API (Serializer)
    - user_id
    - body
    - created_at
    - like_counts
 - Post Update API
    - body 받아서 수정 후 Detail 과 동일한 리턴
 - Post Delete API
    - post_id 에 해당하는 값 제거
"""

from rest_framework import generics
from post.models import Post
from post.serializers import PostListCreateSerializer, PostUpdateDeleteSerializer


class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListCreateSerializer


class PostDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'post_id'

    queryset = Post.objects.all()
    serializer_class = PostUpdateDeleteSerializer
