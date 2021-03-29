from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from post.models import Post


def profile_upload_to(instance, filename):
    return 'user/{}/profile/{}'.format(instance.id, filename)


class UserQuerySet(models.QuerySet):
    def test(self):
        return self.filter(phone_number__isnull=False)


class UserManager(models.Manager.from_queryset(UserQuerySet)):
    def create(self, password, **kwargs):
        user = self.model(**kwargs)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=13)
    email = models.EmailField(max_length=254)
    description = models.TextField()
    like_posts = models.ManyToManyField('post.Post', related_name='like_users')
    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    profile_image = models.ImageField(upload_to=profile_upload_to, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def count_followings(self):
        return self.followings.count()

    def count_followers(self):
        return self.followers.count()

    def count_posts(self):
        return Post.objects.filter(user=self.id).count()
