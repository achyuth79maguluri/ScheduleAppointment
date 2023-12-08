from django import forms
from django.contrib.auth.models import User
from .models import TeacherProfile, StudentProfile

class TeacherRegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    mobile = forms.CharField(max_length=15)
    category = forms.CharField(max_length=50)
    type = forms.CharField(max_length=50)
    location = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'mobile', 'category', 'type', 'location']

class StudentRegistrationForm(forms.ModelForm):
    student_number = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'student_number']
