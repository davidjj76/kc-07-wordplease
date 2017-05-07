from django.views.generic import ListView

from blogs.models import Post


class PostList(ListView):

    template_name = 'blogs/latest_posts.html'
    context_object_name = 'latest_posts'
    queryset = Post.objects.published()
