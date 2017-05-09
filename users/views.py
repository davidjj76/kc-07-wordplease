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
