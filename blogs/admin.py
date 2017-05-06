from django.contrib import admin

from blogs.models import Category, Blog, Post

admin.site.register((Category, Blog, Post))
