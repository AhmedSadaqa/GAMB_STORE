from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
import re


#This is the views

def home(request):
    return render(request, "store/home.html")


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'store/register.html', {'form': form})



@login_required
def profile(request):
    return render(request, 'store/profile.html')


def about(request):
    return render(request, 'store/about.html')


def termOfServices(request):
    return render(request, 'store/termOfServices.html')
    


