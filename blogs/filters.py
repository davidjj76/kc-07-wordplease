import django_filters

from blogs.models import Post


class PostFilter(django_filters.FilterSet):

    category = django_filters.CharFilter(name='categories')

    class Meta:
        model = Post
        fields = ('category',)
