from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
class StudentRegistration(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username']
class UserEditForm(UserChangeForm):
    password = None
    class Meta:
        model=User
        fields=['first_name','last_name','username']
class AdminEditForm(UserChangeForm):
    class Meta:
        model=User
        fields='__all__'
