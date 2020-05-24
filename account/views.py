from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,LoginForm,UserEditForm,ProfileEditForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,authenticate
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout,login,authenticate
from .decorators import unaunth_user
from post.views import *
from django.urls import reverse
# Create your views here.

@unaunth_user
def user_login(request):
  if request.method == "POST":
      form = LoginForm(request.POST)
      if form.is_valid():
          cd = form.cleaned_data
          user = authenticate(request, username=cd['username'],
                                       password=cd['password'])
          if user is not None:
              if user.is_active:
                  login(request, user)
                  return redirect('post:post_list_view')
              else:
                  return HttpResponse("Account is Disabled")
          else:
              messages.warning(request,"Invalid Username and Password")

  else:
      form = LoginForm()
  return render(request,'registration/login.html',{'form':form})

@unaunth_user
def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data.get('username')
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            messages.success(request,f'Account created for {username}!')
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form':user_form})

@login_required
def dashboard(request):
    return render(request,'account/dashboard.html')

def logout_function(request):
    logout(request)
    messages.success(request,'Successfully Logged Out.')
    return redirect('login')

def edit(request):
    if request.method == "POST":
        # profile = Profile.objects.create(user=request.user)
        data = Profile.objects.filter(user=request.user)
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"Profile Updated Success.")
        else:
            messages.error(request,"Error On Updating")
    else:
        # profile = Profile.objects.create(user=request.user)
        data = Profile.objects.filter(user=request.user)
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'account/edit.html',{'user_form':user_form,'profile_form':profile_form,'data':data})
