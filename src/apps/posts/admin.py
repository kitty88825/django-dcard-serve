from django.contrib import admin

from .models import Attachment, Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "creator")


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
