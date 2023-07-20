from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str_(self):
        return self.name
