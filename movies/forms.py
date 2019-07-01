from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class DownloadForm(forms.Form):
    search = forms.CharField()
    option = forms.Select()
