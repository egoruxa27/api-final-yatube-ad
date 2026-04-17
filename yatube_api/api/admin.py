from django.contrib import admin
from posts.models import Comment, Follow, Group, Post

# Register your models here.
admin.site.register(Group)
admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(Comment)
