from django.views.generic import TemplateView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404,redirect
from student.models import Appointment
from login.models import TeacherProfile
from login.models import StudentProfile
from student.forms import AppointmentForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.http import JsonResponse


def quick_appointment(request):
    group_name = Group.objects.all().filter(user=request.user)
    group_name = str(group_name[0])

    if "Teacher" == group_name:
        user_name = request.user.get_username()

        try:
            # Retrieve the teacher's category from the TeacherProfile model
            teacher_profile = TeacherProfile.objects.get(user=request.user)
            teacher_category = teacher_profile.category
            teacher_type = teacher_profile.type
            teacher_first_name = teacher_profile.first_name
            # Filter appointments based on the teacher's category
            appointment_list = Appointment.objects.filter(category=teacher_category, type=teacher_type, first_name=teacher_first_name).order_by("-user")

        except TeacherProfile.DoesNotExist:
            teacher_category = None
            appointment_list = []

        # Other code for filtering by teacher's name, etc.
        # ...

        q = request.GET.get("q")
        if q:
            appointment_list = appointment_list.filter(date__icontains=q)
        student_email = request.GET.get("email")
        
        try:
            # Fetch the student's profile, but handle the case where it may not exist
            student_profile = StudentProfile.objects.get(user=request.user)
            student_number = student_profile.student_number
        except StudentProfile.DoesNotExist:
            # Provide default values if the profile does not exist
            student_profile = None
            student_number = None

        appointments = {
            "query": appointment_list,
            "user_name": user_name,
            "teacher_category": teacher_category,
            "teacher_type": teacher_type,
            "teacher_first_name": teacher_first_name,
            "student_email": student_email,
            "student_number": student_number,
        }

        return render(request, 'faculty_quick_appointment.html', appointments)
    else:
        return redirect('http://127.0.0.1:8000/')

def faculty(request):
    group_name = Group.objects.all().filter(user=request.user)
    group_name = str(group_name[0])

    if "Teacher" == group_name:
        user_name = request.user.get_username()

        try:
            # Retrieve the teacher's category from the TeacherProfile model
            teacher_profile = TeacherProfile.objects.get(user=request.user)
            teacher_category = teacher_profile.category
            teacher_type = teacher_profile.type
            teacher_first_name = teacher_profile.first_name
            # Filter appointments based on the teacher's category
            appointment_list = Appointment.objects.filter(category=teacher_category, type=teacher_type, first_name=teacher_first_name, is_approved=1).order_by("-user")

    
        
        except TeacherProfile.DoesNotExist:
            teacher_category = None
            appointment_list = []

        # Other code for filtering by teacher's name, etc.
        # ...
        # Search by date
        q = request.GET.get("q")

        if q:
            appointment_list = appointment_list.filter(date__icontains=q)
        appointments = {
            "query": appointment_list,
            "user_name": user_name,
            "teacher_category": teacher_category,
            "teacher_type": teacher_type,
            "teacher_first_name": teacher_first_name,
        }

        return render(request, 'faculty.html', appointments)
    else:
        return redirect('http://127.0.0.1:8000/')
# def teacher(request):#this section for my appointment
# 	group_name=Group.objects.all().filter(user = request.user)# get logget user grouped name
# 	group_name=str(group_name[0]) # convert to string
# 	if "Teacher" == group_name:
# 		user_name=request.user.get_username()#Getting Username
# 		#Getting all Post and Filter By Logged UserName
# 		appointment_list = Appointment.objects.all().order_by("-id").filter(appointment_with=user_name)
# 		q=request.GET.get("q")#search start
# 		if q:
# 			appointment_list=appointment_list.filter(user__first_name__icontains=q)
# 		else:
# 			appointment_list = appointment_list# search end

# 		appointments= {
# 		    "query": appointment_list,
# 		    "user_name":user_name,    
# 		}
# 		return render(request, 'teacher.html', appointments )
# 	else:
# 		return redirect('http://127.0.0.1:8000/')

def appointment_book(request, id):#activate after clicking book now button
	group_name=Group.objects.all().filter(user = request.user)# get logget user grouped name
	group_name=str(group_name[0]) # convert to string
	if "Teacher" == group_name:
		user_name=request.user.get_username()
		single_appointment= Appointment.objects.get(id=id)
		form = single_appointment
		form.appointment_with=user_name
		form.save()
		#return HttpResponseRedirect (instance.get_absolute_url())
		#messages.success(request, 'Your profile was updated.')
		return redirect('http://127.0.0.1:8000/teacher/')
	else:
		return redirect('http://127.0.0.1:8000/')

def update_appointment_approval(request, appointment_id):
    if request.method == 'POST':
        try:
            appointment = Appointment.objects.get(pk=appointment_id)
            appointment.is_approved = True
            appointment.save()
            return JsonResponse({'success': True})
        except Appointment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Appointment not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})