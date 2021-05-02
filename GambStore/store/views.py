from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, Book, Application, Game, Movie, CastMember, CreditMemeber, Review
from django.contrib.auth.decorators import login_required
import re
import datetime
from django.db.models import Q
from django.http import Http404
from decimal import *



def home(request):
    books = Book.objects.all()
    applications = Application.objects.all()
    games = Game.objects.all()
    movies = Movie.objects.all()
    currency = "USD"
    context = {"books":books,
               "applications":applications,
               "games":games,
               "movies":movies,
               "currency": currency}
    if request.method == "POST":
        currency = request.POST.get('currency')
        context = {"books":books,
                "applications":applications,
                "games":games,
                "movies":movies, 
                "currency": currency}
        return render(request, "store/GAMBindex.html", context)

    return render(request, "store/GAMBindex.html", context)


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
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'store/profile.html', context)


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
        similarBooks = Book.objects.filter(Genre = books.Genre)
        print(books)
    except Book.DoesNotExist:
        return render(request, 'store/error.html')
    
    context = {"books" : books,
                "similarBooks" : similarBooks}
    return render(request, 'store/selectedBook.html', context)


def applicationItem(request , app_id):
    try:
        app = Application.objects.get(id=app_id)
        similarApps = Application.objects.filter(Genre = app.Genre)
        print(app)
    except app.DoesNotExist:
        return render(request, 'store/error.html')
    
    context = {"app" : app,
                "similarApps" : similarApps}
    return render(request, 'store/selectedApp.html', context)
    

def gameItem(request , game_id):
    try:
        game = Game.objects.get(id=game_id)
        similarGames = Game.objects.filter(Genre = game.Genre)
        print(game)
    except game.DoesNotExist:
        return render(request, 'store/error.html')
    
    context = {"game" : game,
                "similarGames" : similarGames}
    return render(request, 'store/selectedGame.html', context)


def movieItem(request , movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
        similarMovies = Movie.objects.filter(Genre = movie.Genre)
        print(movie)
    except movie.DoesNotExist:
        return render(request, 'store/error.html')
    
    context = {"movie" : movie,
                "similarMovies" : similarMovies}
    return render(request, 'store/selectedMovie.html', context)
