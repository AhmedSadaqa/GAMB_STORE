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
    books = Book.objects.all()
    applications = Application.objects.all()
    games = Game.objects.all()
    movies = Movie.objects.all()
    if request.method == "POST":
        currency = request.POST.get('currency')
        if currency == "LBP":

            print("HII")
        else:
            print("BYE")
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
    return render(request , 'store/bookItem.html')

def bookCategory(request):

    # #Top selling
    # booksOrdered = Book.objects.all().order_by('-CopiesSold')
    # topSelling = []
    # # this is the functionality for the top selling, you should have 10 books in your database to test it or it will give you an error list index out of range
    # for i in range(10):
    #     topSelling.append(booksOrdered[i])
        
    # New Releases Books
    today = datetime.datetime.now()
    current_year = today.year
    last_year = current_year - 1
    
    newReleasesBooks = Book.objects.filter(Q(Date__year=current_year) | Q(Date__year = last_year))

    tenNewReleasesBooks = []
    # for i in range(10):
    #     tenNewReleasesBooks.append(newReleasesBooks[i])
    
    # All Books
    allBooks = Book.objects.all()
    context = {"newReleasesBooks" : newReleasesBooks,
               "allBooks": allBooks,
               }
    return render(request, 'store/bookCategory.html', context)
    

def topSellingBooks(request):
    booksOrdered = Book.objects.all().order_by('-CopiesSold')
    context = {"booksOrdered" : booksOrdered}
    return render(request, 'store/topSellingBooks.html', context)

def newReleases(request):
    today = datetime.datetime.now()
    current_year = today.year
    last_year = current_year - 1
    
    newReleasesBooks = Book.objects.filter(Q(Date__year=current_year) | Q(Date__year = last_year))

    context = {"newReleasesBooks" : newReleasesBooks}
    return render(request, 'store/newReleasesBooks.html', context)

def recommendations(request):
    return render(request, 'store/booksRecommendations.html')

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
