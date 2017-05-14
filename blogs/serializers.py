from django.utils.timezone import now
from rest_framework import serializers

from blogs.models import Post


class PostListSerializer(serializers.ModelSerializer):

    class Meta:

        model = Post
        fields = (
            'title',
            'intro',
            'image',
        )


class PostCreateSerializer(PostListSerializer):

    publish_date = serializers.DateTimeField(default=now())

    class Meta(PostListSerializer.Meta):

        fields = (
            'title',
            'intro',
            'body',
            'image',
            'publish_date',
            'categories',
        )