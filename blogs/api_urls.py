# -*- coding: utf-8 -*-
from django.conf.urls import url

from blogs.api import PostList, PostReply

urlpatterns = [
    url(r'^1.0/posts/?$', PostList.as_view()),
    url(r'^1.0/posts/(?P<pk>[0-9]+)/reply/?$', PostReply.as_view()),
]
