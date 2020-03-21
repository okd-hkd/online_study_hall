from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, EditProfileForm
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'authenticate/home.html',{})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
          login(request, user)

          messages.success(request, 'you have been logged in!')
          
          return redirect('home')
        else:
          
          messages.success(request, 'Error logging in - Please try again')
          return redirect ('login')

    else:
      return render(request, 'authenticate/login.html',{})


def logout_user(request):
  logout(request)
  messages.success(request, 'You have been logged out')
  return redirect('home')


def register_user(request):
    user = SignUpForm(request.POST or None)

    if request.method == 'POST':

      if user.is_valid():
        user.save()

        username = user.cleaned_data['username']
        password = user.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, ('You Have Successfully Registered.'))
        return redirect('home')
          
    else:
        user = SignUpForm()
         
    context = {"form": user}
    return render(request, 'authenticate/register.html', context)



def edit_profile(request):
  # passing the user's infomation
    user = EditProfileForm(request.POST, instance=request.user)
    if request.method == 'POST':
      if user.is_valid():
        user.save()
        messages.success(request, ('You Have Successfully Edited Your Profile.'))
        return redirect('home')
      
    else:
        user = EditProfileForm(instance=request.user)

         
    context = {"form": user}
    return render(request, 'authenticate/edit_profile.html',context)


def change_password(request):
    if request.method == 'POST':
      form = PasswordChangeForm(data=request.POST, user=request.user)
      if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        messages.success(request, ('You Have Successfully Edited Your Profile.'))
        return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {"form": form}
    return render(request, 'authenticate/change_password.html',context)
