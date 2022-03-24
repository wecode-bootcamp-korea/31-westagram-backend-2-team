from django.db import models

class Post(models.Model):
    content    = models.CharField(max_length=2000, null=True)
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "posts"

class Image(models.Model):
    url = models.URLField(max_length=2000)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    class Meta:
        db_table = "images"