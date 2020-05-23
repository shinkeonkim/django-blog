# Generated by Django 3.0.6 on 2020-05-23 11:41

import BlogApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='rep_img_url',
        ),
        migrations.AddField(
            model_name='blog',
            name='rep_img',
            field=models.ImageField(default=None, upload_to=BlogApp.models.date_upload_to),
        ),
    ]
