from django.views.generic import TemplateView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404,redirect
from .models import Appointment
from .forms import AppointmentForm
from login.models import TeacherProfile, StudentProfile
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


def student(request):#this section for my appointment
	group_name=Group.objects.all().filter(user = request.user)# get logget user grouped name
	group_name=str(group_name[0]) # convert to string
	if "Student" == group_name:
		user_name=request.user.get_username()#Getting Username

		#Getting all Post and Filter By Logged UserName
		appointment_list = Appointment.objects.all().order_by("-id").filter(user=request.user)
		q=request.GET.get("q")#search start
		if q:
			appointment_list=appointment_list.filter(first_name__icontains=q)
		else:
			appointment_list = appointment_list# search end

		appointments= {
		    "query": appointment_list,
		    "user_name":user_name
		}
		return render(request, 'student.html', appointments )
	else:
		return redirect('http://127.0.0.1:8000/') 

def student_appointment_list(request):
    group_name = Group.objects.all().filter(user=request.user)
    group_name = str(group_name[0])

    if "Student" == group_name:
        user_name = request.user.get_username()

        selected_category = request.GET.get("category")
        selected_topic = request.GET.get("type")

        unique_users = TeacherProfile.objects.all()
        unique_categories = TeacherProfile.objects.values_list('category', flat=True).distinct()
        unique_topics = TeacherProfile.objects.values_list('type', flat=True).distinct()

        # Get all appointments for the current user
        appointment_list = Appointment.objects.filter(user=request.user)

        q = request.GET.get("q")
        if q:
            appointment_list = appointment_list.filter(date__icontains=q)

        # Get the email and student number of the currently logged-in student
        student_email = request.user.email
        student_profile = StudentProfile.objects.get(user=request.user)
        student_number = student_profile.student_number

        appointments = {
            "query": appointment_list,
            "user_name": user_name,
            "form": AppointmentForm(initial={'email': student_email, 'student_number': student_number}),
            "unique_categories": unique_categories,
            "unique_topics": unique_topics,
            "unique_users": unique_users,
        }

        if request.method == 'POST':
            form = AppointmentForm(request.POST)
            if form.is_valid():
                appointment = form.save(commit=False)
                appointment.user = request.user
                appointment.email = student_email
                appointment.student_number = student_number
                appointment.save()
                messages.success(request, 'Appointment Created Successfully')

        return render(request, 'student_create_appointment.html', appointments)
    else:
        return redirect('http://127.0.0.1:8000/')

  
def appointment_delete(request, id):
	group_name=Group.objects.all().filter(user = request.user)# get logget user grouped name
	group_name=str(group_name[0]) # convert to string
	if "Student" == group_name:
		single_appointment= Appointment.objects.get(id=id)
		single_appointment.delete()
		messages.success(request, 'Your profile was updated.')
		return redirect('http://127.0.0.1:8000/student/create_appointment/')
	else:
		return redirect('http://127.0.0.1:8000/')

def student_appointment_update(request,id):
	group_name=Group.objects.all().filter(user = request.user)# get logget user grouped name
	group_name=str(group_name[0]) # convert to string
	if "Student" == group_name:
		user_name=request.user.get_username()#Getting Username

		#Getting all Post and Filter By Logged UserName
		selected_topic = request.GET.get("type")
		selected_category = request.GET.get("category")
		unique_users = TeacherProfile.objects.all()
		unique_categories = TeacherProfile.objects.values_list('category', flat=True).distinct()
		unique_topics = TeacherProfile.objects.values_list('type', flat=True).distinct()
		appointment_list = Appointment.objects.all().order_by("-id").filter(user=request.user)
		q=request.GET.get("q") #search start
		if q:
			appointment_list=appointment_list.filter(date__icontains=q)
		else:
			appointment_list = appointment_list #search end

		single_appointment=ingle_appointment= Appointment.objects.get(id=id)
		form = AppointmentForm(request.POST or None, instance=single_appointment)
		if form.is_valid():
			    saving=form.save(commit=False)
			    saving.user=request.user
			    saving.save()
			    messages.success(request, 'Post Created Sucessfully')
			    return redirect('http://127.0.0.1:8000/student/create_appointment/')
			    

		appointments= {
		    "query": appointment_list,
		    "user_name":user_name,
		    "form":form,
			"unique_categories": unique_categories,
            "unique_topics": unique_topics,
            "unique_users": unique_users,  # Pass the filtered users to the template
		}

		return render(request, 'student_appointment_update.html', appointments )
	else:
		return redirect('http://127.0.0.1:8000/')


