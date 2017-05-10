from django.conf.urls import url

from users.views import SignupView, LoginView, LogoutView, SignupSuccessfulView, ProfileUpdatedView, ProfileView

urlpatterns = [
    url(r'^profile/?$', ProfileView.as_view(), name="users_profile"),
    url(r'^profile/updated/?$', ProfileUpdatedView.as_view(), name="users_profile_updated"),
    url(r'^signup/?$', SignupView.as_view(), name="users_signup"),
    url(r'^signup/successful/?$', SignupSuccessfulView.as_view(), name="users_signup_successful"),
    url(r'^login/?$', LoginView.as_view(), name="users_login"),
    url(r'^logout/?$', LogoutView.as_view(), name="users_logout"),
]
