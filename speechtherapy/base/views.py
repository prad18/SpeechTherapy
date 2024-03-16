from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
# Create your views here.

def loginPage(request):
    page = 'login'
    if request.method=="POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
             messages.error(request, "User doesn't exist!")
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('letters')
        else:
            messages.error(request, "Username or Password is incorrect!")

    context={'page':page}
    return render(request, 'login.html', context)

def registerPage(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            username = form.cleaned_data.get('username')
            return redirect('letters')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")


    return render(request, 'login.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='home')
def learn(request):
        return render(request, 'base/learn.html')

def register(request):
    return render(request,'register.html')

@login_required(login_url='home')
def letters(request):
    return render(request,'base/letters.html')

