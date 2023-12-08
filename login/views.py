from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from login.forms import TeacherRegistrationForm, StudentRegistrationForm
from .models import TeacherProfile, StudentProfile
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def group_check(request):
    group_name = Group.objects.all().filter(user=request.user)  # get the logged-in user's group name
    group_name = str(group_name[0])  # convert to string

    if "Student" == group_name:
        return redirect('http://127.0.0.1:8000/student/')
    elif "Teacher" == group_name:
        return redirect('http://127.0.0.1:8000/faculty/')

def logout_view(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')

def register_faculty(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            mobile = form.cleaned_data['mobile']
            category = form.cleaned_data['category']
            type = form.cleaned_data['type']
            location = form.cleaned_data['location']
            first_name = form.cleaned_data['first_name']
            # Create a new User
            user = User.objects.create_user(username=username, password=password, email=email)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            # Create a TeacherProfile
            teacher_profile = TeacherProfile(user=user, mobile=mobile, category=category, type=type, location=location, first_name=first_name)
            teacher_profile.save()

            # Add the user to the 'Teacher' group
            teacher_group = Group.objects.get(name='Teacher')
            teacher_group.user_set.add(user)

            # Log the user in after registration
            login(request, user)

            return redirect('http://127.0.0.1:8000/faculty')

    else:
        form = TeacherRegistrationForm()

    return render(request, 'register_faculty.html', {'form': form})

def check_username_availability(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        is_taken = User.objects.filter(username=username).exists()
        return JsonResponse({'is_taken': is_taken})
    else:
        return JsonResponse({'error': 'Invalid request method'})


# Add similar views for email and mobile availability checks
def check_email_availability(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        is_taken = User.objects.filter(email=email).exists()
        
        if is_taken:
            message = 'This email is already taken. Please choose another one.'
        else:
            message = ''

        return JsonResponse({'is_taken': is_taken, 'message': message})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def check_mobile_availability(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile', '')
        is_taken = TeacherProfile.objects.filter(mobile=mobile).exists()
        
        if is_taken:
            message = 'This mobile number is already taken. Please choose another one.'
        else:
            message = ''

        return JsonResponse({'is_taken': is_taken, 'message': message})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def check_student_number_availability(request):
    if request.method == 'POST':
        student_number = request.POST.get('student_number', '')
        is_taken = StudentProfile.objects.filter(student_number=student_number).exists()
        
        if is_taken:
            message = 'This student number is already taken. Please choose another one.'
        else:
            message = ''

        return JsonResponse({'is_taken': is_taken, 'message': message})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            student_number = form.cleaned_data['student_number']
            
            # Create a new User
            user = User.objects.create_user(username=username, password=password, email=email)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            
            # Create a StudentProfile
            student_profile = StudentProfile(user=user, student_number=student_number)
            student_profile.save()

            # Add the user to the 'Student' group
            student_group = Group.objects.get(name='Student')
            student_group.user_set.add(user)

            # Log the user in after registration
            login(request, user)
            
            return redirect('http://127.0.0.1:8000/student')  # Replace 'your-success-url' with the URL where you want to redirect after successful registration
    else:
        form = StudentRegistrationForm()

    return render(request, 'register_student.html', {'form': form})
