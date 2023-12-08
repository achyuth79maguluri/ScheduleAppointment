# forms.py
from django import forms

class ChangeStatusForm(forms.Form):
    STATUS_CHOICES = [
        (0, 'Pending'),
        (1, 'Approved'),
        (2, 'On-Hold'),
        (3, 'Reject'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES)
