from django.db import models


def user_upload_to(instance, filename):
    return 'user/{}/posts/{}'.format(instance.user.id, filename)


class Post(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField(upload_to=user_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    body = models.TextField()
