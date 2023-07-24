from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


def index(request):
    return render(request, 'task_manager/index.html')


class LoginUser(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'task_manager/login.html'
    success_message = _('You are logged in')


class LogoutUser(SuccessMessageMixin, LogoutView):

    def get(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().get(request, *args, **kwargs)
