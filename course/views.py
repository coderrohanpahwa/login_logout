from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
from django.contrib import messages
from .forms import StudentRegistration
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import logout,login,authenticate,update_session_auth_hash
from .forms import UserEditForm
from .forms import AdminEditForm
from django.contrib.auth.models import User
def sign(request):

        if request.method=="POST":
            fm=StudentRegistration(request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request,"You can login now")
        else:
            fm=StudentRegistration()
        return render(request,'course/signup.html',{'forms':fm})

def log(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upass=fm.cleaned_data['password']
                user=authenticate(request,username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,"You have successfully logged in")
                    return HttpResponseRedirect('/profile/')
            else:
                messages.error(request,"Username and password do not match in our database . Make sure you write them correctly. If you are new you can signup")
        else:
            fm=AuthenticationForm()
        return render(request,'course/login.html',{'forms':fm})
    else:
       return HttpResponseRedirect('/profile/')
def profile(request):
    obj=None
    if request.user.is_authenticated:
        if request.method=="POST":
            if request.user.is_superuser:
                fm=AdminEditForm(request.POST,instance=request.user)
                obj=User.objects.all()

            else:
                fm=UserEditForm(request.POST,instance=request.user)
            if fm.is_valid():
                    fm.save()
                    messages.success(request,"You have successfully updated your details")
        else:
            if request.user.is_superuser:
                fm=AdminEditForm(request.POST,instance=request.user)
                obj=User.objects.all()

            else:
                fm=UserEditForm(instance=request.user)

        return render(request,'course/profile.html',{'name':request.user,'forms':fm,'info':obj})
    else:
        messages.error(request,"You must login first")
        return HttpResponseRedirect('/login/')
def change_pass(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            fm=SetPasswordForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request,fm.user)
                messages.success(request,"You have successfully updated your password")
                return HttpResponseRedirect('/profile/')
        else:
            fm=SetPasswordForm(user=request.user)
        return render(request, 'course/change_pass.html', {'forms': fm})
    else:
        messages.error(request,"You must login")
        return render(request,'/login/')
def out(request):
    logout(request)
    messages.success(request,"You have successfully logged out")
    return HttpResponseRedirect('/login/')
def update(request,my_id):
    if request.user.is_superuser:
        if request.method=="POST":
            pi=User.objects.get(pk=my_id)
            fm=AdminEditForm(request.POST,instance=pi)
            if fm.is_valid():
                fm.save()
                messages.success(request,"You have successfully updated details")
        else:
                pi=User.objects.get(pk=my_id)
                fm=AdminEditForm(instance=pi)
        return render(request,'course/update.html',{'forms':fm})
    else:
        messages.error(request,"You arent a super user")
        return HttpResponseRedirect('/login/')