#coding=utf8

from django import forms
from models import Trip, Tag

class TripForm(forms.ModelForm):

    class Meta:
        fields = ('name', 'date_start', 'date_end')
        model = Trip
        help_texts = {
            'date_start': 'dd.mm.yyyy',
            'date_end': 'dd.mm.yyyy',
        }

class TagForm(forms.ModelForm):
    class Meta:
        fields = ('text', )
        model = Tag
        help_texts = {'text': 'help', }
