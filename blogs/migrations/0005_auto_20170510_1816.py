# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-10 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_remove_post_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blogs/images'),
        ),
    ]
