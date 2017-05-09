from django.conf.urls import url
from django.contrib import admin

from blogs.views import PostList, BlogList, BlogDetail, PostDetail
from users.views import SignupView, LoginView, LogoutView, SignupSuccessfulView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', PostList.as_view(), name='latest_posts'),
    url(r'^blogs/?$', BlogList.as_view(), name='blog_list'),
    url(r'^blogs/(?P<username>[a-zA-Z0-9_]+)/?$', BlogDetail.as_view(), name="blog_detail"),
    url(r'^blogs/(?P<username>[a-zA-Z0-9_]+)/(?P<pk>[0-9]+)/?$', PostDetail.as_view(), name="post_detail"),
    url(r'^signup/?$', SignupView.as_view(), name="users_signup"),
    url(r'^signup/successful/?$', SignupSuccessfulView.as_view(), name="users_signup_successful"),
    url(r'^login/?$', LoginView.as_view(), name="users_login"),
    url(r'^logout/?$', LogoutView.as_view(), name="users_logout"),
]
