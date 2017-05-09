from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.urls import reverse
from django.views.generic import FormView

from users.forms import UserForm


class SignupView(FormView):

    template_name = 'users/signup.html'
    form_class = UserForm

    def get_success_url(self):
        return reverse('latest_posts')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LoginView(DjangoLoginView):

    template_name = 'users/login.html'

    def get_success_url(self):
        return self.request.GET.get('next', reverse('latest_posts'))


class LogoutView(DjangoLogoutView):

    def get_next_page(self):
        return reverse('users_login')
