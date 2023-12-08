from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from student.models import Appointment
from login.models import TeacherProfile
from datetime import datetime, timedelta

def update_appointment_status(request, appointment_id):
    if request.method == 'POST':
        try:
            appointment = get_object_or_404(Appointment, pk=appointment_id)
            status = request.POST.get("status")

            if status in ["0", "1", "2", "3"]:
                appointment.is_approved = int(status)
                appointment.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid status'})
        except Appointment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Appointment not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})

    return JsonResponse({'success': False})

def update_teacher_comment(request, appointment_id):
    if request.method == 'POST':
        try:
            appointment = get_object_or_404(Appointment, pk=appointment_id)
            comment = request.POST.get("comment")
            appointment.teacher_comment = comment
            appointment.save()
            return JsonResponse({'success': True})
        except Appointment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Appointment not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})

def update_teacher_room(request, appointment_id):
    if request.method == 'POST':
        try:
            appointment = get_object_or_404(Appointment, pk=appointment_id)
            room = request.POST.get("room")
            appointment.room_number = room
            appointment.save()
            return JsonResponse({'success': True})
        except Appointment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Appointment not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})

def get_filtered_users(request):
    selected_category = request.GET.get('category')
    selected_topic = request.GET.get('type')
    
    users = TeacherProfile.objects.filter(category=selected_category, type=selected_topic)
    user_data = {user.user.first_name: user.user.username for user in users}
    
    return JsonResponse(user_data)


def get_filtered_types(request):
    selected_category = request.GET.get('category')
    
    types = TeacherProfile.objects.filter(category=selected_category).values_list('type', flat=True).distinct()
    
    return JsonResponse(list(types), safe=False)

def get_teacher_slots(request, teacher_id):
    try:
        # Get the teacher's appointment schedule
        teacher_appointments = Appointment.objects.filter(appointment_with=teacher_id)

        # Define the start and end times of the day
        workday_start_time = datetime.strptime('08:00 AM', '%I:%M %p').time()
        workday_end_time = datetime.strptime('05:00 PM', '%I:%M %p').time()

        # Define the duration of each time slot (e.g., 30 minutes)
        time_slot_duration = timedelta(minutes=30)

        # Initialize lists to store available and unavailable slots
        available_slots = []
        unavailable_slots = []

        # Create a list of all time slots in the workday
        current_time = datetime.combine(datetime.now().date(), workday_start_time)
        end_time = datetime.combine(datetime.now().date(), workday_end_time)

        while current_time < end_time:
            slot_start_time = current_time.time()
            slot_end_time = (current_time + time_slot_duration).time()

            # Check if the slot is in the teacher's appointments
            slot_in_appointments = False
            for appointment in teacher_appointments:
                appointment_start_time = datetime.strptime(appointment.time_start, '%I:%M %p').time()
                appointment_end_time = datetime.strptime(appointment.time_end, '%I:%M %p').time()

                if appointment_start_time <= slot_start_time < appointment_end_time or \
                   appointment_start_time < slot_end_time <= appointment_end_time:
                    slot_in_appointments = True
                    break

            if slot_in_appointments:
                unavailable_slots.append({
                    'start_time': slot_start_time.strftime('%I:%M %p'),
                    'end_time': slot_end_time.strftime('%I:%M %p')
                })
            else:
                available_slots.append({
                    'start_time': slot_start_time.strftime('%I:%M %p'),
                    'end_time': slot_end_time.strftime('%I:%M %p')
                })

            current_time += time_slot_duration

        # Return the available and unavailable slots as JSON response
        response_data = {
            'available_slots': available_slots,
            'unavailable_slots': unavailable_slots
        }
        return JsonResponse(response_data)

    except Exception as e:
        # Handle exceptions here (e.g., teacher not found)
        response_data = {
            'error': str(e)
        }
        return JsonResponse(response_data)
