from django.shortcuts import render

from blogs.models import Post


def index(request):
    latest_posts = Post.objects.all()
    context = {
        'latest_posts': latest_posts
    }
    return render(request, 'blogs/latest_posts.html', context)
