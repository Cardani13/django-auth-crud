from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Basicamente se crea la tabla que almacena las tareas y sus campos para llenarla
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)  #se agrega por defeccto
    datecompleted = models.DateTimeField(null=True, blank =True) # solo opcional con blank para el admin
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title + '- by ' + self.user.username
