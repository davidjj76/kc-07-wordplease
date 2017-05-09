from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from blogs.filters import PostFilter
from blogs.forms import PostForm
from blogs.models import Post, Blog, Category


class PostQuerySet:

    def get_queryset(self):
        return PostFilter(self.request.GET, queryset=Post.objects.published()).qs.select_related('blog__owner')


class BlogContextData:

    @staticmethod
    def get_by_username(username):
        return {
            'categories': Category.objects.all(),
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
            BlogContextData.get_by_username(self.kwargs.get('username'))
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


class NewPost(LoginRequiredMixin, CreateView):

    model = Post
    form_class = PostForm
    template_name = 'blogs/new_post.html'
    login_url = reverse_lazy('users_login')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.method == 'POST':
            form.instance.blog = self.request.user.blog
        return form

    def get_success_url(self):
        post = self.object
        return reverse('post_detail', kwargs={
            'username': post.blog.owner.username,
            'pk': post.pk,
        })
