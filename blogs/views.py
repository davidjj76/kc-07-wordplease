from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
    def get_blog(username):
        return {
            'username': username,
            'blog': get_object_or_404(Blog, owner__username=username)
        }

    @staticmethod
    def get_categories():
        return {
            'categories': Category.objects.all(),
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
            BlogContextData.get_blog(self.kwargs.get('username'))
        )
        context.update(
            BlogContextData.get_categories()
        )
        return context


class PostDetail(PostQuerySet, DetailView):

    template_name = 'blogs/post_detail.html'

    def get_queryset(self):
        return super().get_queryset().filter(blog__owner__username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            BlogContextData.get_blog(self.kwargs.get('username'))
        )
        return context


class NewPost(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    model = Post
    form_class = PostForm
    template_name = 'blogs/new_post.html'

    def test_func(self):
        # para poder publicar un post, además de logado, el usuario debe de tener blog
        try:
            return self.request.user.blog
        except Blog.DoesNotExist:
            return False

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

    def get_login_url(self):
        if self.request.user.is_authenticated:
            return reverse('users_profile')
        else:
            return reverse('users_login')


class PostReply(NewPost):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'replied_post': get_object_or_404(Post, pk=self.kwargs.get('pk'))
        })
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.method == 'POST':
            form.instance.reply_to = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return form

