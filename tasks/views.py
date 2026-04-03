from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate #login para crear la cookie por nosotros
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,  'home.html')

def signup(request):
    
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #register user
                user = User.objects.create_user(
                    username=request.POST['username'], 
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exist'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'who that fuck is NigaNigga (password not match)'
        })

@login_required    
def tasks(request):
    #tasks = Task.objects.all()
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)#Solo tareas del usuario actual y que esten vacias
    return render(request, 'tasks.html', {'tasks': tasks}) #Pasar el dato al front

@login_required
def signout(request):
    logout(request)
    return redirect('home')  

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'who that fuck is GigaNigga (Username or password is incorrect)'
            })
        else:
            login(request, user)
            return redirect('tasks')  
@login_required        
def create_task(request):
    
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else :
        try:
            # formulario para guardar los datos 
            form = TaskForm(request.POST)
            new_task = form.save(commit=False) #solo para devolver los datos de esta nueva tarea
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:   #Validacion de algun error
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Plese provide valid data'
            })
@login_required            
def task_detail(request, task_id):
    if request.method == 'GET':
        #task = Task.objects.get_or(pk=task_id) lo mismo que abajo pero sin validacion
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task) #Llenara el formulario con la tarea
        
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user) #obtener la tarea relacionada con el id
            form = TaskForm(request.POST, instance=task) #Pasamos al formulario lo que obtenemos del form (una instancia)
            form.save()  #Actualiza el formulario
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'error': 'Error updating task',
                'form': form
            })
@login_required            
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required    
def tasks_completed(request):
    title = "Tasks Completed" #agregación para que marque el completed en el titulo
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by
    ('-datecompleted')#Solo tareas del usuario actual y que esten completas
    return render(request, 'tasks.html', {'tasks': tasks, 'title': title}) #Pasar el dato al front