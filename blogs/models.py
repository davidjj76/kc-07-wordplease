from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.datetime_safe import datetime


class Category(models.Model):

    name = models.CharField(max_length=250, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Blog(models.Model):

    owner = models.OneToOneField(User,related_name='blog')
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250, blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class PostManager(models.Manager):

    def published(self):
        return Post.objects.filter(publish_date__lte=datetime.now())


class Post(models.Model):

    blog = models.ForeignKey(Blog, related_name='posts')
    title = models.CharField(max_length=250)
    intro = models.TextField(max_length=250)
    body = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    publish_date = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(Category, related_name='posts')
    objects = PostManager()

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.title
