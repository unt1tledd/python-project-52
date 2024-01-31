from django.shortcuts import render
from task_manager.users.models import CustomUser
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from task_manager.users.forms import CustomUserCreationForm


#class Index(SuccessMessageMixin, CreateView):
   #model = CustomUser
    #form_class = CustomUserCreationForm
    #template_name = 'tgbot/file.html'
def index(request):
    return render(request, 'tgbot/file.html')
