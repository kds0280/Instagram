from django.db import models


def user_upload_to(instance, filename):
    return 'user/{}/posts/{}'.format(instance.user.id, filename)


class Post(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField(upload_to=user_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)

    def two_comments(self):
        return self.comments.filter(parent__isnull=True)[:2]

    def all_comments(self):
        return self.comments.filter(parent__isnull=True)

    def count_like(self):
        return self.like_users.count()


class Comment(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='children')
    body = models.TextField()
