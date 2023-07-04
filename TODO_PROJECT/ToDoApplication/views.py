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
    # this is the home page view function, to display todolist home page
    if request.method == 'GET':
        return render(request, 'ToDoList.html')
    else:
        return redirect('/')

@csrf_exempt
def login_view(request):
    """
    login view function to handle login user login functionality
    POST: check the username and password, and authenticate the user
    GET: check if user is alredy login then redirect user to the home page and show the login view page

    params: username and password
    """
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
    
@csrf_exempt
def register_view(request):
    """
    register view function to handle new user registration functionality
    POST: check the username, pass and other field, and login the user
    GET: check if user is alredy login then redirect user to the registration page and show the registration page

    """
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
    """
    API call to get all task details of logged in user
    return: it returns all task details into json format

    """
    tasks = Task.objects.filter(user = request.user).order_by('task_priority')
    task_data_list = []
    for task in tasks:
        temp_dict = {
            'id': task.id,
            'task_title' :  task.task_title,
            'task_status': task.get_task_status_display(),
            'task_priority': task.get_task_priority_display(),
            'task_description' : task.task_description
        }
        task_data_list.append(temp_dict)
    # return JsonResponse({'tasks': list(tasks.values())})
    return JsonResponse({'tasks': task_data_list})


@csrf_exempt
def add_task(request):

    """
    API call for add task using POST method:
    get all task data and create the new task data to the database and also check the validations
    and return appropriate message into JSON response

    """
    
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
        # if not description:
        #     errors['description'] = 'Description is required'
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

    """
    API call for get the particular task or update the particular task using taskID
    args: TaskID - to get the particular task details

    POST: get the updated task details using taskID and save it into out db and return the success message
    GET: get the task details using taskID and return it into json response
    """


    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        # Retrieve the updated task details from the request
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        status = request.POST.get('status')

        # Update the task with the new details

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

    """
    API call for deleting a particular task
    args: takes taskID to get the task and delete it and return appropriate message
    """

    # Retrieve the task object
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

    """
    Function to logout the current user 
    """
    logout(request)
    return redirect('/')

def filter_by_priority(request):
    """
    Fetches tasks based on the selected priority via AJAX call.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A JsonResponse containing the task data if the priority is valid,
      otherwise an error message.
    """
    priority = request.GET.get('priority')

    if priority:
        if priority == "0":
            tasks = Task.objects.filter(user = request.user).order_by("task_priority")
        else:
            tasks = Task.objects.filter(user = request.user, task_priority=priority)

        task_data = []
        for task in tasks:
            task_data.append({
                'task_title': task.task_title,
                'task_description': task.task_description,
                'task_status': task.get_task_status_display(),
                'user': task.user.username,
                'task_priority': task.get_task_priority_display(),
            })
        return JsonResponse({'tasks': task_data})
    
    return JsonResponse({'error': 'Invalid priority value'})

def filter_by_status(request):
    """
    Fetches tasks based on the selected status via AJAX call.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A JsonResponse containing the task data if the status is valid,
      otherwise an error message.
    """
    status = request.GET.get('status')

    if status:
        if status == "0":
            tasks = Task.objects.filter(user = request.user).order_by("task_priority")
        else:
            tasks = Task.objects.filter(user = request.user, task_status=status).order_by("task_priority")

        task_data = []
        for task in tasks:
            task_data.append({
                'task_title': task.task_title,
                'task_description': task.task_description,
                'task_status': task.get_task_status_display(),
                # 'task_status': dict(Task.STATUS_CHOICES).get(task.task_status),
                # 'task_priority': dict(Task.PRIORITY_CHOICES).get(task.task_priority),
                'user': task.user.username,
                'task_priority': task.get_task_priority_display(),
            })
        return JsonResponse({'tasks': task_data})
    
    return JsonResponse({'error': 'Invalid priority value'})