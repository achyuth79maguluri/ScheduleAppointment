from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("login.urls")),
    path('student/', include("student.urls")),
    path('faculty/', include("teacher.urls")),
    path('update_appointment_status/<int:appointment_id>/', views.update_appointment_status, name='update_appointment_status'),
    path('get_filtered_users/', views.get_filtered_users, name='get_filtered_users'),
    path('get_filtered_types/', views.get_filtered_types, name='get_filtered_types'),
    path('get_teacher_slots/<int:teacher_id>/', views.get_teacher_slots, name='get_teacher_slots'),
    path('update_teacher_comment/<int:appointment_id>/', views.update_teacher_comment, name='update_teacher_comment'), # Fix here
    path('update_teacher_room/<int:appointment_id>/', views.update_teacher_room, name='update_teacher_room'), # Fix here
]
