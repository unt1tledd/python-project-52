from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Task
from django_filters.views import FilterView
from task_manager.tasks.filter import TaskFilter
from task_manager.tasks.forms import TaskForm
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.utils.translation import gettext_lazy as _
from task_manager.right_user import NewLoginRequiredMixin, TaskPassesTestMixin


class TaskListView(FilterView):
    model = Task
    template_name = 'tasks/tasks.html'
    filterset_class = TaskFilter
    context_object_name = 'tasks'


class CreateTaskView(NewLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTaskView(NewLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully updated')


class DeleteTaskView(TaskPassesTestMixin, NewLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully deleted')


class TaskDetailView(SuccessMessageMixin, DetailView):
    model = Task
    template_name = 'tasks/task.html'
