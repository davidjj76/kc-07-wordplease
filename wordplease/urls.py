from django.conf.urls import url
from django.contrib import admin

from blogs.views import PostList

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', PostList.as_view(), name='latest_posts')
]
