from django.contrib.auth.views import LoginView
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .models import *
from django.views.generic import *
from django.http import JsonResponse


def get_filtered_streams(request):
    class_id = request.GET.get('class_id')
    streams = Stream.objects.filter(class_name_id=class_id).values('id', 'name')
    return JsonResponse({'streams': list(streams)})

@user_passes_test(lambda u: u.user_type == 'admin', login_url='users:login')
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'User {username} has been created successfully.')
            return redirect('main:dashboard_admin')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = UserRegisterForm()

    return render(request, 'adminstrator/create_student.html', {'form': form})

def custom_login(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                auth_login(request, user)
                if user.user_type == 'student':
                    return redirect("main:dashboard")
                elif user.user_type == 'admin':
                    return redirect("main:dashboard_admin")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error) 

    form = UserLoginForm()

    return render(
        request=request,
        template_name="users/index.html",
        context={"form": form}
    )


def custom_logout(request):
    logout(request)
    messages.info(request, "succesfully logged out")
    return redirect("users:login")
    
@login_required
def create_teacher(request):
    if request.method == 'POST':
        form = TeacherCreationForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, 'Teacher created successfully.')
            return redirect('users:teachers')  # Redirect to the TeacherListView
    else:
        form = TeacherCreationForm()

    return render(request, 'adminstrator/create_teacher.html', {'form': form})

class teachers(ListView):
    model = Teacher
    template_name = 'adminstrator/teachers.html'
    context_object_name = 'teachers'

def student(request):
    User = get_user_model()
    students = User.objects.filter(user_type='student')

    return render(request, 'adminstrator/student.html', {'students': students})

def create_parent(request):
    if request.method == 'POST':
        form = ParentCreationForm(request.POST)
        if form.is_valid():
            parent = form.save(commit=False)
            parent.user = request.user  # Assign the current user as the parent's user
            parent.save()
            form.save_m2m()  # Save the many-to-many relationships, if any
            messages.success(request, 'Parent created successfully.')
            return redirect('users:parents')  # Redirect to parent list page
        else:
            messages.error(request, 'Error creating parent. Please check the form.')
    else:
        form = ParentCreationForm()
    
    return render(request, 'adminstrator/create_parent.html', {'form': form})

def parents(request):
    parents = Parent.objects.all()
    return render(request, 'adminstrator/parents.html', {'parents': parents})

def classes(request):
    classes = ClassName.objects.all()
    return render(request, 'adminstrator/classes.html', {'classes': classes})