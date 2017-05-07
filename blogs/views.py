from django.db.models import Count
from django.views.generic import ListView, DetailView

from blogs.models import Post, Blog


class PostList(ListView):

    template_name = 'blogs/latest_posts.html'
    queryset = Post.objects.published().select_related('blog__owner')


class PostDetail(DetailView):

    model = Post
    template_name = 'blogs/post_detail.html'


class BlogList(ListView):

    template_name = 'blogs/blog_list.html'
    queryset = Blog.objects.annotate(num_posts=Count('posts')).select_related('owner')


class BlogDetail(PostList):

    template_name = 'blogs/blog_detail.html'

    def get_queryset(self):
        return super().queryset.filter(blog__owner__username=self.kwargs.get('username'))