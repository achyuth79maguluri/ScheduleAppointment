from django.db import models
from django.contrib.auth.models import User

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    category = models.CharField(max_length=50, default='DefaultCategory')
    type = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, default='DefaultValue')
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_number = models.CharField(max_length=15)
    email = models.CharField(max_length=50, default='DefaultValue')