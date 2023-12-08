from django.urls import path
from . import views

urlpatterns = [
    path('', views.faculty, name='faculty'),
    path('my_appointment/', views.faculty, name='faculty'),
    path('quick_appointment/', views.quick_appointment, name='quick_appointment'),   
    path('update/<int:id>/', views.appointment_book, name='appointment_update'),
    path('teacher/quick-appointment/<str:teacher_name>/', views.quick_appointment, name='teacher_quick_appointment'),
]