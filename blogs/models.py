from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


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

    def __str__(self):
        return self.name

class Post(models.Model):

    blog = models.ForeignKey(Blog, related_name='posts')
    title = models.CharField(max_length=250)
    intro = models.TextField(max_length=250)
    body = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    publish_date = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(Category, related_name='posts')

    def __str__(self):
        return self.title
