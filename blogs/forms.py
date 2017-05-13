from django import forms
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from blogs.models import Post, Category


class PostForm(forms.ModelForm):

    title = forms.CharField(label=_('Title'), max_length=250)
    intro = forms.CharField(label=_('Intro'), widget=forms.Textarea, max_length=250)
    body = forms.CharField(label=_('Body'), widget=forms.Textarea)
    image = forms.ImageField(label=_('Image'), required=False)
    publish_date = forms.DateTimeField(label=_('Publish date'), initial=now())
    categories = forms.ModelMultipleChoiceField(label=_('Categories'), queryset=Category.objects.all())

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

