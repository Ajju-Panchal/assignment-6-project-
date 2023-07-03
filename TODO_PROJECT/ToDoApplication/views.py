from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from .models import Task
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def index(request):
    print("insde-------------------")
    tasks = Task.objects.filter(user=request.user)


    # print("FINAL TASK LIST : {}".format(task_data_list))
    # Get the selected filter options
    # priority_filter = request.GET.get('priority', '')
    # status_filter = request.GET.get('status', '')
    
    # Apply filters
    # if priority_filter:
        # tasks = tasks.filter(priority=priority_filter)
    # if status_filter:
        # tasks = tasks.filter(status=status_filter)
    
    # Sort tasks by priority (high to low)
    tasks = tasks.order_by('-task_priority')
    
    return render(request, 'ToDoList.html', {'tasks': tasks})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Input field validations
        if not username or not password:
            messages.error(request, 'Please fill in all fields')
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'ToDoList.html')  # Redirect to the home page after successful login
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('/')
        # form = AuthenticationForm()
        return render(request, 'userLogin.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['password1']
        email = request.POST['email']
        phone = request.POST['phone']

        # Input field validations
        if not username or not password or not email or not phone or not confirm_password:
            messages.error(request, 'Please fill in all fields')
            return redirect('register')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')
        
        # Create a new user object
        user = User.objects.create_user(username=username, password=password, email=email)

        # Add additional user details to the user profile
        # user.profile.phone = phone
        # user.profile.save()

        # Log in the user
        login(request, user)

        # messages.success(request, 'Registration successful. You are now logged in.')

        return render(request, 'ToDoList.html')  # Redirect to the home page after successful registration

    else:
        if request.user.is_authenticated:
            return redirect('/')
        # form = UserCreationForm()
        return render(request, 'userRegistration.html')


def get_task_list(request):
    print("inside task list")
    tasks = Task.objects.filter(user = request.user)
    task_data_list = []
    for task in tasks:
        temp_dict = {
            'id': task.id,
            'task_title' :  task.task_title,
            'task_status': dict(Task.STATUS_CHOICES).get(task.task_status),
            'task_priority': dict(Task.PRIORITY_CHOICES).get(task.task_priority),
            'task_description' : task.task_description
        }
        task_data_list.append(temp_dict)
    print(task_data_list)
    # return JsonResponse({'tasks': list(tasks.values())})
    return JsonResponse({'tasks': task_data_list})

    
def edit_data(request, id):
    obj = get_object_or_404(Task, id=id)

    if request.method == 'POST':
        field1 = request.POST.get('field1')
        field2 = request.POST.get('field2')
        priority = request.POST.get('priority')
        status = request.POST.get('status')

        obj.field1 = field1
        obj.field2 = field2
        obj.priority = priority
        obj.status = status

        obj.save()
        return redirect('home')

    return render(request, 'edit.html', {'obj': obj})

def delete_data(request, id):
    obj = get_object_or_404(Task, id=id)

    if request.method == 'POST':
        obj.delete()
        return redirect('home')

    return render(request, 'delete.html', {'obj': obj})

@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        # Retrieve the task details from the request
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')

        # Perform form validation
        errors = {}

        # Check if required fields are not empty
        if not title:
            errors['title'] = 'Title is required'
        if not description:
            errors['description'] = 'Description is required'
        if not priority:
            errors['priority'] = 'Priority is required'

        # If there are errors, return them as JSON response
        if errors:
            return JsonResponse({'errors': errors}, status=400)

        # Create a new task object
        task = Task(user = request.user, task_title=title, task_description=description, task_priority=priority)
        task.save()

        # Return a success JSON response
        return JsonResponse({'message': 'Task added successfully'})
    else:
        return JsonResponse({'errors': 'Invalid Method!'}, status=400)

@csrf_exempt
def get_or_edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        print("INSIDE EDIT TASK----------")
        # Retrieve the updated task details from the request
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        status = request.POST.get('status')

        print("----------")
        print(title)
        print(description)
        print(priority)

        # Update the task with the new details
        print(task.id)
        task.task_title = title
        task.task_description = description
        task.task_priority = priority
        task.task_status = status
        task.save() 

        # Return a success JSON response
        return JsonResponse({'message': 'Task updated successfully'})

    # If it's a GET request, return the task details as JSON response
    task_data = {
        'title': task.task_title,
        'description': task.task_description,
        'priority': task.task_priority,
        'status': task.task_status
    }
    return JsonResponse(task_data)

@csrf_exempt
def delete_task(request, task_id):
    # Retrieve the task object
    print("inside delete task")
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        # Perform the deletion
        task.delete()
        # Return a JSON response indicating success
        return JsonResponse({'message': 'Task deleted successfully.'})
    else:
        # Return a JSON response with an error message
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
def logout_view(request):
    logout(request)
    return redirect('/')