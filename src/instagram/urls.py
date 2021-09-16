from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from post.views import PostListCreate, PostDetailUpdateDelete, CommentCreate, CommentDelete, PostLike
from user.views import Login, SignUp, UserUpdate, UserFollow, UserProfile, Search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search', Search.as_view(), name='search'),
    path('post', PostListCreate.as_view()),
    path('post/<int:post_id>', PostDetailUpdateDelete.as_view()),
    path('post/<int:post_id>/like', PostLike.as_view(), name='likepost'),
    path('auth', Login.as_view(), name='login'),
    path('signup', SignUp.as_view(), name='signup'),
    path('user/<int:user_id>', UserUpdate.as_view()),
    path('user/<int:user_id>/detail', UserProfile.as_view()),
    path('user/<int:user_id>/follow', UserFollow.as_view()),
    path('comment', CommentCreate.as_view()),
    path('comment/<int:comment_id>', CommentDelete.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
