from django.shortcuts import render


def index(request):
    return render(request, 'blogs/latest_posts.html')

