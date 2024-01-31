from task_manager.tg_bot import views
from django.urls import path


urlpatterns = [
    path('', views.index)
]
