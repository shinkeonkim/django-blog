from django.db import models
import os
from uuid import uuid4
from django.utils import timezone

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
    rep_img = models.ImageField(upload_to=date_upload_to, default = None)
    published_at = models.DateTimeField()
    body = models.TextField()
    hashtag = models.TextField()

    def __str__(self):
        return self.title

    