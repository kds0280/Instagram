from django.db import models


class Post(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    like_count = models.IntegerField(default=0)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    body = models.TextField()
