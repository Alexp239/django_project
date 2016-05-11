from django import forms
from models import Trip

class TripForm(forms.ModelForm):

    class Meta:
        fields = ('name', 'date_start', 'date_end')
        model = Trip
