from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.users.forms import CustomUserCreationForm
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from task_manager.tasks.models import Task
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.right_user import NewLoginRequiredMixin, UserPermissionMixin


class RegisterUser(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')



class UserListView(ListView):
    model = CustomUser
    template_name = 'users/list_users.html'
    context_object_name = 'users'
    extra_context = {'btn_update': _('Update'),
                     'btn_delete': _('Delete'),
                     }


class UpdateUserView(SuccessMessageMixin, UpdateView, NewLoginRequiredMixin, UserPermissionMixin):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    success_message = _('User successfully updated')


class DeleteUserView(SuccessMessageMixin, DeleteView, NewLoginRequiredMixin, UserPermissionMixin):
    model = CustomUser
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    success_message = _('User successfully deleted')
        
    def post(self, request, *args, **kwargs):
        self_id = self.kwargs['pk']
        if Task.objects.filter(
                Q(executor_id=self_id) | Q(author_id=self_id)):
            messages.error(
                self.request,
                _('It`s not possible to delete a User that is being used')
            )
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
