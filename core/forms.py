from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Project, Task

BS = {'class': 'form-control'}
BS_SELECT = {'class': 'form-select'}


class SignupForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.Select(attrs=BS_SELECT))

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs=BS),
            'email': forms.EmailInput(attrs=BS),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs=BS)
        self.fields['password2'].widget = forms.PasswordInput(attrs=BS)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs=BS),
            'description': forms.Textarea(attrs={**BS, 'rows': 3}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assigned_to', 'status', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs=BS),
            'description': forms.Textarea(attrs={**BS, 'rows': 3}),
            'project': forms.Select(attrs=BS_SELECT),
            'assigned_to': forms.Select(attrs=BS_SELECT),
            'status': forms.Select(attrs=BS_SELECT),
            'due_date': forms.DateInput(attrs={**BS, 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        # Accept an optional `user` kwarg to pre-select assigned_to
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Make assigned_to required and remove the empty choice
        self.fields['assigned_to'].required = True
        self.fields['assigned_to'].empty_label = None
        if user and not self.instance.pk:
            self.initial.setdefault('assigned_to', user.pk)


class TaskStatusForm(forms.ModelForm):
    """Minimal form for members to update only status."""
    class Meta:
        model = Task
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs=BS_SELECT),
        }
