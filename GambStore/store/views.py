from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Profile, Book, Application, Game, Movie, CastMember, CreditMemeber, Review
from django.contrib.auth.decorators import login_required
import re
import datetime
from django.db.models import Q
from django.http import Http404



def home(request):
    return render(request, "store/GAMBindex.html")


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
    return render(request, 'store/ToS.html')
    
def item(request):
    return render(request , 'store/item.html')

def bookCategory(request):

    #Top selling


    # New Releases Books
    today = datetime.datetime.now()
    current_year = today.year
    last_year = current_year - 1
    
    newReleasesBooks = Book.objects.filter(Q(Date__year=current_year) | Q(Date__year = last_year))


    # All Books
    allBooks = Book.objects.all()



    context = {"newReleasesBooks" : newReleasesBooks,
               "allBooks": allBooks,
               }
    return render(request, 'store/bookCategory.html', context)
    

def applicationCategory(request):
    applications = Application.objects.all()
    context = {"applications" : applications}
    return render(request, 'store/bookCategory.html', context)
    

def gameCategory(request):
    games = Game.objects.all()
    context = {"games" : games}
    return render(request, 'store/bookCategory.html', context)
    

def movieCategory(request):
    movies = Movie.objects.all()
    context = {"movies" : movies}
    return render(request, 'store/bookCategory.html', context)
    

def bookItem(request, book_id):
    try:
        books = Book.objects.get(id=book_id)
        print(books)
    except Book.DoesNotExist:
        return render(request, 'store/error.html')
    
    context = {"books" : books}
    return render(request, 'store/bookItem.html', context)


def applicationItem(request):
    applications = Application.objects.all()
    context = {"applications" : applications}
    return render(request, 'store/bookItem.html', context)
    

def gameItem(request):
    games = Game.objects.all()
    context = {"games" : games}
    return render(request, 'store/bookItem.html', context)


def movieItem(request):
    movies = Movie.objects.all()
    context = {"movies" : movies}
    return render(request, 'store/bookItem.html', context)
