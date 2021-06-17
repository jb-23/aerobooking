from django import forms
from django.forms import ModelForm
from .models import Booking

# Create the form class.

def time_choices_generator():
    x = []
    for t in range(830, 1831, 100):
        x.append( (str(t), f"{t//100:02d}:{t%100:02d}") )
    return x


class BookingUserForm(ModelForm):
    finish_time = forms.ChoiceField(widget=forms.Select, choices=time_choices_generator(), initial=1430)

    class Meta:
        model = Booking
        fields = ['date', 'aircraft', 'start_time', 'finish_time', 'type', 'remarks']
        widgets = {
            'start_time': forms.Select(choices=time_choices_generator()),
            'remarks': forms.Textarea(),
        }


class BookingAdminForm(ModelForm):
    finish_time = forms.ChoiceField(widget=forms.Select, choices=time_choices_generator(), initial=1430)

    class Meta:
        model = Booking
        fields = ['date', 'aircraft', 'member', 'start_time', 'finish_time', 'type', 'authorised', 'remarks']
        widgets = {
            'start_time': forms.Select(choices=time_choices_generator()),
            'remarks': forms.Textarea(),
        }
