from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.users.forms import CustomUserCreationForm
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


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


class UpdateUserView(SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    success_message = _('User successfully updated')


class DeleteUserView(SuccessMessageMixin, DeleteView):
    model = CustomUser
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    success_message = _('User successfully deleted')
        
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        user = CustomUser.objects.get(id=user_id)
        return render(request, 'users/delete.html', {'user': user})
    
    def post(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        user = CustomUser.objects.get(id=user_id)
        if user:
            user.delete()
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
        
