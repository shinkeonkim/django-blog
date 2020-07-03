from django.db import models
import os
from uuid import uuid4
from django.utils import timezone
from django.conf import settings

def date_upload_to(instance, filename):
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()
    return '/'.join([
        ymd_path,
        uuid_name + extension,
        ])

class Blog(models.Model):
    title = models.CharField(max_length = 200)
    publisher = models.CharField(max_length=50)
    rep_img = models.ImageField(upload_to=date_upload_to, blank = True, default = None)
    published_at = models.DateTimeField()
    body = models.TextField()
    hashtag = models.TextField(blank = True, default = None)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likers', blank=True, through='Like')

    def __str__(self):
        return self.title

    def title_summary(self):
        add = ""
        if len(self.title) > 10:
            add = "..."
        return self.title[:10] + add 

    def summary(self):
        add = ""
        if len(self.body) > 20:
            add = "..."
        return self.body[:20] + add 

    def hashtag_summary(self):
        add = ""
        if len(self.hashtag) > 15:
            add = "..."
        return self.hashtag[:15] + add

    def like_count(self):
        return self.like_users.count()


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null = True, blank = True, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author} 님이 {self.blog}에 단 댓글"


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)