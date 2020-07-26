from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,get_user_model
from django.contrib import  auth
from .forms import LoginForm,RegisterForm


# Create your views here.

User = get_user_model()



def signup(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        new_user =  User.objects.create_user(username,email,password,first_name=first_name,last_name=last_name)
        print(new_user)
    return render(request, 'accounts/signup.html',{'form' : form})


def Login(request):
       form = LoginForm(request.POST or None)
       if request.method == 'POST':

         form = LoginForm(request.POST or None)
         print(request.user.is_authenticated)
         print(form.is_bound)
         print(form.is_valid())
         if form.is_valid():
            print(form.cleaned_data)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')


            print(request.user.is_authenticated)
            user = authenticate(request,username=username,password=password)
            if user is not  None:
                auth.login(request,user)
                return redirect('homme')
            else:
                error = 'Wrong password or username !'
                return render(request, 'accounts/login.html', {'form': form,'er':error})
         else:
             print(form.errors)
             print('invalid')
       return render(request,'accounts/login.html',{'form' : form})


def logout(request):
     if request.method == 'POST':
            auth.logout(request)
            return redirect('login')

     return redirect('login')
