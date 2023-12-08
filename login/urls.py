from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', LoginView.as_view(template_name='index.html'), name="home"),
    path('logout/', views.logout_view, name='logout'),
    path('group/', views.group_check, name='group'),
    path('check_username_availability/', views.check_username_availability, name='check_username_availability'),
    path('check_email_availability/', views.check_email_availability, name='check_email_availability'),
    path('check_mobile_availability/', views.check_mobile_availability, name='check_mobile_availability'),
    path('check_student_number_availability/', views.check_student_number_availability, name='check_student_number_availability'),
    path('register_faculty/', views.register_faculty, name='register_faculty'),  # Remove .as_view()
    path('register_student/', views.register_student, name='register_student'),  # Remove .as_view()
]
