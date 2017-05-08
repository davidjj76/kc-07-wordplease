from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from blogs.models import Post, Blog, Category


class PostQuerySet:

    def get_queryset(self):
        return Post.objects.published().select_related('blog__owner')


class BlogContextData:

    @staticmethod
    def get_by_username(username, get_categories):
        return {
            'categories': Category.objects.all() if get_categories else None,
            'username': username,
            'blog': get_object_or_404(Blog, owner__username=username)
        }


class PostList(PostQuerySet, ListView):

    template_name = 'blogs/latest_posts.html'

    def get_queryset(self):
        return super().get_queryset()


class BlogList(ListView):

    template_name = 'blogs/blog_list.html'
    queryset = Blog.objects.annotate(num_posts=Count('posts')).select_related('owner')


class BlogDetail(PostQuerySet, ListView):

    template_name = 'blogs/blog_detail.html'

    def get_queryset(self):
        return super().get_queryset().filter(blog__owner__username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            BlogContextData.get_by_username(self.kwargs.get('username'), True)
        )
        return context


class PostDetail(PostQuerySet, DetailView):

    template_name = 'blogs/post_detail.html'

    def get_queryset(self):
        return super().get_queryset().filter(blog__owner__username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            BlogContextData.get_by_username(self.kwargs.get('username'))
        )
        return context
