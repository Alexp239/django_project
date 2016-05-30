#coding=utf8

from django import forms
from models import Trip, Tag, Person

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

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField()

    class Meta:
        fields = ('username', 'password', 'email', 'city_from', 'country', 'first_name', 'last_name')
        model = Person
        help_texts = {'text': 'Одно слово, состоящее из маленьких букв и цифр', }

    def clean_username(self):
        username = self.cleaned_data['username']
        if Person.objects.filter(username=username).count() != 0:
            raise forms.ValidationError("Это имя уже занято")
        return username

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', "Пароли не совпадают")
            self.add_error('password', "")

class SettingForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'email', 'city_from', 'country', 'phone', 'vk_id', 'text')
