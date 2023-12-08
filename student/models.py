from django.db import models
from django.conf import settings

# Database creation for teacher appointment.
class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, default='')
    first_name = models.CharField(max_length=150, default='')
    date = models.CharField(max_length=50)
    time_start = models.CharField(max_length=50)
    time_end = models.CharField(max_length=50)
    room_number = models.CharField(max_length=50)
    appointment_with = models.CharField(max_length=50, blank=True)
    update_time = models.DateField(auto_now=True, auto_now_add=False)
    frist_time = models.DateField(auto_now=False, auto_now_add=True)
    category = models.CharField(max_length=50, default='DefaultCategory')
    type = models.CharField(max_length=50, default='DefaultType')
    is_approved = models.IntegerField(choices=[(0, 'Pending'), (1, 'Approved'), (2, 'On-Hold'), (3, 'Reject')], default=0)
    reason = models.CharField(max_length=50, default='DefaultReason')
    student_number = models.PositiveIntegerField(default=0)
    email = models.CharField(max_length=50, default='DefaultValue')
    teacher_comment = models.TextField(null=True, blank=True)
    def __str__(self):
        return f'Date: {self.date}, Time: {self.time_start} - {self.time_end}, Room Number: {self.room_number}, Appointment With: {self.appointment_with}'
