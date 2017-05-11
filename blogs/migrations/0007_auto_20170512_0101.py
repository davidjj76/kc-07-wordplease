# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-11 23:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogs', '0006_auto_20170510_2313'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post_Mentions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail_sent_at', models.DateTimeField(null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='mentions',
            field=models.ManyToManyField(null=True, related_name='mentions', through='blogs.Post_Mentions', to=settings.AUTH_USER_MODEL),
        ),
    ]