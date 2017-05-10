from django.forms import ModelForm

from blogs.models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = (
            'title',
            'intro',
            'body',
            'image',
            'publish_date',
            'categories',
        )

