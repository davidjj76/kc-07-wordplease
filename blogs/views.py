from django.views.generic import ListView

from blogs.models import Post, Blog


class PostList(ListView):

    template_name = 'blogs/latest_posts.html'
    context_object_name = 'latest_posts'
    queryset = Post.objects.published()


class BlogList(ListView):

    model = Blog
    template_name = 'blogs/blog_list.html'
