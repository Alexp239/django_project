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
        help_texts = {'text': 'Одно слово, состоящее из маленьких букв и цифр', }

    def clean_text(self):
        data = self.cleaned_data['text']
        if len(data) <= 1:
             raise forms.ValidationError("Пустой тег")
        for i in range(0, len(data)):
            c = data[i]
            if (i == 0):
                if c != '#':
                    raise forms.ValidationError("Тег должен начинаться с #")
                    break
            else:
                if not ((c >= 'a' and c <= 'z') or (c >= u'а' and c <= u'я') or (c >= '0' and c <= '9')):
                    raise forms.ValidationError("Недопустимые символы")
                    break
        return data
