from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    username = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=13)
    email = models.EmailField(max_length=254)
    description = models.TextField()
    like_posts = models.ManyToManyField('post.Post', related_name='like_users')
    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)

    def get_username(self):
        return self.username
