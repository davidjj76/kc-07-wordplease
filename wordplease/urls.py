from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from blogs import urls as blogs_urls, api_urls as blogs_api_urls
from users import urls as users_urls
from wordplease import settings

urlpatterns = [
    # Django Admin URLs
    url(r'^admin/', admin.site.urls),

    # Blogs URLs
    url(r'^', include(blogs_urls)),

    # Users URLs
    url(r'^', include(users_urls)),

    # API URLs
    url(r'^api/', include(blogs_api_urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
