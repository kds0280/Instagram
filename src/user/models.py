from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


def profile_upload_to(instance, filename):
    return 'user/{}/profile/{}'.format(instance.id, filename)


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=13)
    email = models.EmailField(max_length=254)
    description = models.TextField()
    like_posts = models.ManyToManyField('post.Post', related_name='like_users')
    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    profile_image = models.ImageField(upload_to=profile_upload_to, null=True)

    USERNAME_FIELD = 'username'
