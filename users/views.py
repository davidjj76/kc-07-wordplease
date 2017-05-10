from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from blogs.models import Blog
from users.forms import UserForm


class SignupProfileView(View):

    template_name = None

    def get_form_initial_data(self, request):
        raise NotImplemented()

    def get_user_object(self):
        return User()

    def get_blog_object(self, user):
        return Blog(owner=user)

    def get_success_url(self):
        raise NotImplemented()

    def get(self, request):
        form = UserForm(initial=self.get_form_initial_data(request))
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user = self.get_user_object()
        form = UserForm(data=request.POST)
        form.instance = user
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.username = form.cleaned_data.get('username')
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            if request.user.is_authenticated():
                update_session_auth_hash(request, user)

            blog = self.get_blog_object(user)
            blog.name = form.cleaned_data.get('blog_name')
            blog.description = form.cleaned_data.get('blog_description')
            blog.save()
            return redirect(self.request.GET.get('next', self.get_success_url()))
        else:
            return render(request, self.template_name, {'form': form})

class SignupView(SignupProfileView):

    template_name = 'users/signup.html'

    def get_form_initial_data(self, request):
        return {}

    def get_success_url(self):
        return 'users_signup_successful'


class SignupSuccessfulView(TemplateView):

    template_name = 'users/signup_successful.html'


class ProfileView(LoginRequiredMixin, SignupProfileView):

    template_name = 'users/profile.html'
    login_url = reverse_lazy('users_login')

    def get_form_initial_data(self, request):
        try:
            blog = request.user.blog
        except Blog.DoesNotExist:
            blog = None

        return {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'username': request.user.username,
            'blog_name': blog.name if blog else '',
            'blog_description': blog.description if blog else ''
        }

    def get_user_object(self):
        return self.request.user

    def get_blog_object(self, user):
        try:
            return user.blog
        except Blog.DoesNotExist:
            return super().get_blog_object(user)

    def get_success_url(self):
        return 'users_profile_updated'


class ProfileUpdatedView(TemplateView):

    template_name = 'users/profile_updated.html'


class LoginView(DjangoLoginView):

    template_name = 'users/login.html'

    def get_success_url(self):
        return self.request.GET.get('next', reverse('users_profile'))


class LogoutView(DjangoLogoutView):

    def get_next_page(self):
        return reverse('users_login')
