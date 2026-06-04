from .forms import SignUpForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.models import User
from django.shortcuts import redirect


class SignUpView(FormView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form: SignUpForm):
        user: User = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect("login")
