from django.db import models

from apps.categories.models import Category
from apps.tags.models import Tag
from apps.users.models import User


def post_attachment_path(instance, filename):
    return f"post_attachment/{instance.post.id}/{filename}"


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="creator_post",
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    like = models.ManyToManyField(User, related_name="like_post")
    collect = models.ManyToManyField(User, related_name="collect_post")

    def __str__(self):
        return f"{self.id}: {self.title}"


class Attachment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="attachments",
    )
    file_path = models.FileField(upload_to=post_attachment_path)


class Comment(models.Model):
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name="like_comment")
