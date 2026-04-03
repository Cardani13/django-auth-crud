from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):  #Para ver un campo de solo lectura se tuvo que crear esta clase
    readonly_fields = ("created", ) 
    

# Register your models here.
admin.site.register(Task, TaskAdmin) #se agrega el Taskadmin al haber creado la case que obtiene todo de admin 