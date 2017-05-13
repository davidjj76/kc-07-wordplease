import sys

import re
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now

from wordplease import settings
from .tasks import resize_thumbnails_update_post_image, send_mail_notification


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
    reply_to = models.ForeignKey(
        'self',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    objects = PostManager()

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('post_detail', args=[self.blog.owner.username, self.pk])

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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if not force_update:
            self.create_notifications()

    def create_notifications(self):
        replied_user = self.reply_to.blog.owner if self.reply_to else None

        # Notificaciones por respuesta
        # Hay un usuario replicado y es distinto al autor del post
        if replied_user and replied_user.id != self.blog.owner.id:
            self.notifications.create(
                post=self,
                receiver=replied_user
            )

        # Notificaciones por mención
        for mention in self.get_mentions():
            mentioned_user = User.objects.filter(username=mention[1:])
            # La mención corresponde a un usuario real, que no es el autor del post ni el usuario replicado
            if len(mentioned_user) == 1 and mentioned_user[0].id != self.blog.owner.id:
                if not replied_user or replied_user.id != mentioned_user[0].id:
                    self.notifications.create(
                        post=self,
                        receiver=mentioned_user[0]
                    )


class Notification(models.Model):
    post = models.ForeignKey(Post, related_name='notifications')
    receiver = models.ForeignKey(User, related_name='notifications')
    mail_sent_at = models.DateTimeField(null=True)

    def send_mail(self):
        post = self.post
        receiver = self.receiver
        if post.reply_to and receiver.id == post.reply_to.blog.owner.id:
            subject = '{0} has replied your post {1}'.format(post.blog.owner.username, post.reply_to.title)
        else:
            subject = '{0} has mentioned you in a new post'.format(post.blog.owner.username)

        send_mail(
            subject,
            post.title + '\n' +
            post.intro + '\n' +
            'Read more on {0}'.format(post.get_url()),
            post.blog.owner.email,
            [receiver.email]
        )

        self.mail_sent_at = now()
        self.save()



if settings.USE_CELERY and 'test' not in sys.argv and 'migrate' not in sys.argv:

    @receiver(post_save, sender=Post)
    def post_saved(sender, **kwargs):
        post = kwargs.get('instance')
        created = kwargs.get('created')

        if created and post:
            if post.image:
                resize_thumbnails_update_post_image.delay(post.pk)


    @receiver(post_save, sender=Notification)
    def notification_saved(sender, **kwargs):
        notification = kwargs.get('instance')
        created = kwargs.get('created')

        if created and notification:
            send_mail_notification.delay(notification.pk)
