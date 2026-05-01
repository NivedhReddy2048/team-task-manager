from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .models import User, Project, Task
from .forms import SignupForm, ProjectForm, TaskForm, TaskStatusForm
from .serializers import ProjectSerializer, TaskSerializer


# ─── Auth Views ──────────────────────────────────────────────────────────────

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'dashboard'))
        else:
            error = 'Invalid username or password.'
    return render(request, 'core/login.html', {'error': error})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# ─── Dashboard ────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    user = request.user
    today = timezone.now().date()

    if user.is_admin:
        tasks = Task.objects.select_related('project', 'assigned_to').all()
    else:
        tasks = Task.objects.select_related('project', 'assigned_to').filter(assigned_to=user)

    total = tasks.count()
    in_progress = tasks.filter(status='In Progress').count()
    completed = tasks.filter(status='Completed').count()
    overdue = tasks.filter(due_date__lt=today).exclude(status='Completed').count()

    projects = Project.objects.all() if user.is_admin else Project.objects.none()

    context = {
        'tasks': tasks.order_by('-created_at'),
        'projects': projects,
        'total': total,
        'in_progress': in_progress,
        'completed': completed,
        'overdue': overdue,
    }
    return render(request, 'core/dashboard.html', context)


# ─── Project Views ────────────────────────────────────────────────────────────

@login_required
def project_create(request):
    if not request.user.is_admin:
        messages.error(request, 'Only admins can create projects.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, f'Project "{project.name}" created!')
            return redirect('dashboard')
    else:
        form = ProjectForm()
    return render(request, 'core/project_form.html', {'form': form, 'title': 'Create Project'})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.select_related('assigned_to').all()
    return render(request, 'core/project_detail.html', {'project': project, 'tasks': tasks})


# ─── Task Views ───────────────────────────────────────────────────────────────

@login_required
def task_create(request):
    if not request.user.is_admin:
        messages.error(request, 'Only admins can create tasks.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created!')
            return redirect('dashboard')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'core/task_form.html', {'form': form, 'title': 'Create Task'})


@login_required
def task_update_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    user = request.user

    # Members can only update tasks assigned to them
    if not user.is_admin and task.assigned_to != user:
        messages.error(request, 'You can only update your own tasks.')
        return redirect('dashboard')

    if request.method == 'POST':
        if user.is_admin:
            form = TaskForm(request.POST, instance=task, user=user)
        else:
            form = TaskStatusForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated!')
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task, user=user) if user.is_admin else TaskStatusForm(instance=task)

    return render(request, 'core/task_form.html', {'form': form, 'title': 'Update Task', 'task': task})


# ─── DRF API ViewSets ─────────────────────────────────────────────────────────

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=user)
