from django.db import models
from task_manager.users.models import CustomUser
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    description = models.TextField(null=True, verbose_name="Описание")
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True)
    executor = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                                 null=True, related_name='executor', verbose_name="Исполнитель")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус")
    labels = models.ManyToManyField(Label,  through='Relation', blank=True, verbose_name="Метка")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

class Relation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    labels = models.ForeignKey(Label, on_delete=models.PROTECT, null=True)
