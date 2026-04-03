from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = { # Para estilizar el formulario creado por mi en esta clase
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a title'}), # Pasa el atributo class de html y la clase de bootstrap
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a description'}), #TextArea porque eso usa html
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }