from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Status
from django.shortcuts import render, redirect
from task_manager.statuses.forms import StatusForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from task_manager.mixin import NewLoginRequiredMixin


def index(request):
    statuses = Status.objects.all()
    return render(request, 'statuses/statuses.html', {'statuses': statuses})


class CreateStatusView(NewLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully created')


class UpdateStatusView(NewLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully updated')


class DeleteStatusView(NewLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully deleted')

    def post(self, request, *args, **kwargs):
        if self.get_object().task_set.count():
            messages.warning(self.request,
                             _('It`s not possible to delete the status that is being used'))
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
