from django.urls import path
from . import views

urlpatterns = [
    path('', views.student, name='student_home'),
    path('my_appointment/', views.student, name='student_appointment'),
    path('create_appointment/', views.student_appointment_list, name='student_appointment_list'),
    path('create_appointment/delete/<int:id>/', views.appointment_delete, name='appointment_delete'),
    path('create_appointment/update/<int:id>/', views.student_appointment_update, name='student_appointment_update'),
]



