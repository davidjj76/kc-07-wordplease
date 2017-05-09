from django.conf.urls import url, include
from django.contrib import admin

from blogs import urls as blogs_urls
from users import urls as users_urls

urlpatterns = [
    # Django Admin URLs
    url(r'^admin/', admin.site.urls),

    # Blogs URLs
    url(r'^', include(blogs_urls)),

    # Users URLs
    url(r'^', include(users_urls)),
]
