from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from post.views import PostListCreate, PostDetailUpdateDelete, CommentCreate, CommentDelete, PostLike
from user.views import Login, SignUp, UserUpdate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post', PostListCreate.as_view()),
    path('post/<int:post_id>', PostDetailUpdateDelete.as_view()),
    path('post/<int:post_id>/like', PostLike.as_view()),
    path('auth', Login.as_view()),
    path('signup', SignUp.as_view()),
    path('user/<int:user_id>', UserUpdate.as_view()),
    path('user/<int:user_id>/follow', UserFollow.as_view()),
    path('comment', CommentCreate.as_view()),
    path('comment/<int:comment_id>', CommentDelete.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
