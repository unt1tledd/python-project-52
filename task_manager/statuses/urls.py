from django.urls import path
from task_manager.statuses import views


urlpatterns = [
    path('', views.index, name='statuses'),
    path('create/', views.CreateStatusView.as_view(), name='create_status'),
    path('<int:pk>/update', views.UpdateStatusView.as_view(), name='update_status'),
    path('<int:pk>/delete', views.DeleteStatusView.as_view(), name='delete_status'),
]

