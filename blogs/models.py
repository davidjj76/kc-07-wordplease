import sys

import re
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from wordplease import settings
from .tasks import resize_thumbnails_update_post_image, generate_mentions_from_post, send_mail_from_post_to_user


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
        return Post.objects.filter(publish_date__lte=timezone.now())


class Post(models.Model):

    blog = models.ForeignKey(Blog, related_name='posts')
    title = models.CharField(max_length=250)
    intro = models.TextField(max_length=250)
    body = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to='blogs/images')
    publish_date = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(Category, related_name='posts')
    mentions = models.ManyToManyField(
        User,
        related_name='mentions',
        null=True,
        through='Post_Mentions',
        through_fields=('post', 'user')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    objects = PostManager()

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.title

    def get_image_extension(self):
        return self.image.name.split('.')[-1]

    def get_image_name(self):
        return ''.join((self.image.name.split('/')[-1]).split('.')[0:-1])

    @staticmethod
    def get_folder(path):
        return '/'.join((path.split('/'))[0:-1])

    def get_absolute_image_folder(self):
        return Post.get_folder(self.image.path)

    def get_relative_image_folder(self):
        return Post.get_folder(self.image.name)

    def get_mentions(self):
        return list(set(re.compile(r'@\w+').findall(self.body)))


class Post_Mentions(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mail_sent_at = models.DateTimeField(null=True)


if settings.USE_CELERY and 'test' not in sys.argv and 'migrate' not in sys.argv:

    @receiver(post_save, sender=Post)
    def post_saved(sender, **kwargs):
        post = kwargs.get('instance')
        created = kwargs.get('created')

        if post and created:
            generate_mentions_from_post.delay(post.pk)

            if post.image:
                resize_thumbnails_update_post_image.delay(post.pk)

    @receiver(post_save, sender=Post_Mentions)
    def post_mention_saved(sender, **kwargs):
        post = kwargs.get('instance').post
        user = kwargs.get('instance').user
        created = kwargs.get('created')

        if post and user and created:
            send_mail_from_post_to_user.delay(post.pk, user.username)
