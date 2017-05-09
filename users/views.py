from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from users.forms import UserForm


class SignupView(View):

    template_name = 'users/signup.html'

    def get(self, request):
        return render(request, self.template_name, { 'form': UserForm() })

    def post(self, request):
        form = UserForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('latest_posts'))

        return render(request, self.template_name, { 'form': form })
