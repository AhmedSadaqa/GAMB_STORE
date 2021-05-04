from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, Book, Application, Game, Movie, CastMember, CreditMemeber, Review, WishList, VisitedItems
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


# BOOKS

def bookCategory(request):
    if request.method == "POST":
        filtering = request.POST.get('filter')
        filteredBooks = Book.objects.filter(Genre=filtering)
        
        return render(request, 'store/filteredBooks.html', {'filteredBooks' : filteredBooks, 'filtering' : filtering})

    # #Top selling
    topSellingbooks = Book.objects.all().order_by('-CopiesSold')
    tenTopSellingBooks = []
    # # this is the functionality for the top selling, you should have 10 books in your database to test it or it will give you an error list index out of range
    for i in range(5):
        tenTopSellingBooks.append(topSellingbooks[i])
        
    # New Releases Books
    today = datetime.datetime.now()
    current_year = today.year
    last_year = current_year - 1
    
    newReleasesBooks = Book.objects.filter(Q(Date__year=current_year) | Q(Date__year = last_year))
    tenNewReleasesBooks = []
    for i in range(5):
        tenNewReleasesBooks.append(newReleasesBooks[i])

    
    #Recommendations

    context = {"tenTopSellingBooks" : tenTopSellingBooks,
               "tenNewReleasesBooks": tenNewReleasesBooks     
            }
    return render(request, 'store/bookCategory.html', context)
    

def topSellingBooks(request):
    topSellingsBooks = Book.objects.all().order_by('-CopiesSold')
    context = {"topSellingsBooks" : topSellingsBooks}
    return render(request, 'store/allTopSellingBooks.html', context)

def newReleasesBooks(request):
    today = datetime.datetime.now()
    current_year = today.year
    last_year = current_year - 1
    
    newReleases = Book.objects.filter(Q(Date__year=current_year) | Q(Date__year = last_year))

    context = {"newReleases" : newReleases}
    return render(request, 'store/allNewReleasesBooks.html', context)

def booksRecommendations(request):
    return render(request, 'store/allBooksRecommendations.html')


def bookItem(request, book_id):
    books = Book.objects.get(id=book_id)
    if request.method == "POST":
        if 'currency' in request.POST:
            currency = request.POST.get('currency')
        else:
            if 'like' in request.POST:
                like = request.POST.get('like')
                review = Review.objects.get(id=like)
                review.likes += 1
                review.save()
            elif 'dislike' in request.POST:
                dislike = request.POST.get('dislike')
                review = Review.objects.get(id=dislike)
                review.dislikes += 1
                review.save()
            elif 'report' in request.POST:
                report = request.POST.get('report')
                review = Review.objects.get(id=report)
                review.report += 1
                if review.report >= 10:
                    review.delete()   
        
    try:
        reviews = Review.objects.filter(book_id=books)
        currency = "USD"
        similarBooks = Book.objects.filter(Genre = books.Genre)
        average_rating = 0
        if reviews:
            for review in reviews:
                average_rating += review.Rating
            average_rating = average_rating/reviews.__len__()
        else:
            average_rating = 0
    except books.DoesNotExist:
        return render(request, 'store/error.html')
    
    context = {"books" : books,
                "similarBooks" : similarBooks,
                "reviews": reviews ,
                "average": average_rating,
                "currency" : currency
                }
    return render(request, 'store/selectedBook.html', context)


# APPLICATIONS

def applicationCategory(request):
    applications = Application.objects.all()
    context = {"applications" : applications}
    return render(request, 'store/applicationCategory.html', context)

def topSellingApplications(request):
    topSellingsApps = Application.objects.all().order_by('-CopiesSold')
    context = {"topSellingsApps" : topSellingsApps}
    return render(request, 'store/allTopSellingsApps.html', context)

def newReleasesApplications(request):
    today = datetime.datetime.now()
    current_year = today.year
    last_year = current_year - 1
    
    newReleasesApps = Application.objects.filter(Q(Date__year=current_year) | Q(Date__year = last_year))

    context = {"newReleasesApps" : newReleasesApps}
    return render(request, 'store/allNewReleasesApps.html', context)

def applicationsRecommendations(request):
    return render(request, 'store/allAppsRecommendations.html')

def applicationItem(request , app_id):
    app = Application.objects.get(id=app_id)
    if request.method == "POST":
        if 'currency' in request.POST:
            currency = request.POST.get('currency')
        else:
            if 'like' in request.POST:
                like = request.POST.get('like')
                review = Review.objects.get(id=like)
                review.likes += 1
                review.save()
            elif 'dislike' in request.POST:
                dislike = request.POST.get('dislike')
                review = Review.objects.get(id=dislike)
                review.dislikes += 1
                review.save()
            elif 'report' in request.POST:
                report = request.POST.get('report')
                review = Review.objects.get(id=report)
                review.report += 1
                if review.report >= 10:
                    review.delete()   
        
    try:
        reviews = Review.objects.filter(application_id=app)
        currency = "USD"
        similarApps = Application.objects.filter(Genre = app.Genre)
        average_rating = 0
        if reviews:
            for review in reviews:
                average_rating += review.Rating
            average_rating = average_rating/reviews.__len__()
        else:
            average_rating = 0
    except app.DoesNotExist:
        return render(request, 'store/error.html')
    
    context = {"app" : app,
                "similarApps" : similarApps,
                "reviews": reviews ,
                "average": average_rating,
                "currency" : currency
                }
    return render(request, 'store/selectedApp.html', context)
    

# GAMES

def gameCategory(request):
    games = Game.objects.all()
    context = {"games" : games}
    return render(request, 'store/gameCategory.html', context)

def topSellingGames(request):
    topSellingsGames = Game.objects.all().order_by('-CopiesSold')
    context = {"topSellingsGames" : topSellingsGames}
    return render(request, 'store/allTopSellingsGames.html', context)

def newReleasesGames(request):
    today = datetime.datetime.now()
    current_year = today.year
    last_year = current_year - 1
    
    newReleases = Game.objects.filter(Q(Date__year=current_year) | Q(Date__year = last_year))

    context = {"newReleases" : newReleases}
    return render(request, 'store/allNewReleasesGames.html', context)

def gamesRecommendations(request):
    return render(request, 'store/allGamesRecommendations.html')

def gameItem(request , game_id):
    game = Game.objects.get(id=game_id)
    if request.method == "POST":
        if 'currency' in request.POST:
            currency = request.POST.get('currency')
        else:
            if 'like' in request.POST:
                like = request.POST.get('like')
                review = Review.objects.get(id=like)
                review.likes += 1
                review.save()
            elif 'dislike' in request.POST:
                dislike = request.POST.get('dislike')
                review = Review.objects.get(id=dislike)
                review.dislikes += 1
                review.save()
            elif 'report' in request.POST:
                report = request.POST.get('report')
                review = Review.objects.get(id=report)
                review.report += 1
                if review.report >= 10:
                    review.delete()   
        
    try:
        reviews = Review.objects.filter(game_id=game)
        currency = "USD"
        similarGames = Game.objects.filter(Genre = game.Genre)
        average_rating = 0
        if reviews:
            for review in reviews:
                average_rating += review.Rating
            average_rating = average_rating/reviews.__len__()
        else:
            average_rating = 0
    except game.DoesNotExist:
        return render(request, 'store/error.html')
    
    context = {"game" : game,
                "similarGames" : similarGames,
                "reviews": reviews ,
                "average": average_rating,
                "currency" : currency
                }
    print(currency)
    return render(request, 'store/selectedGame.html', context)

    
# MOVIES

def movieCategory(request):
    movies = Movie.objects.all()
    context = {"movies" : movies}
    return render(request, 'store/movieCategory.html', context)
    
def topSellingmovies(request):
    topSellingsMovies = Movie.objects.all().order_by('-CopiesSold')
    context = {"topSellingsMovies" : topSellingsMovies}
    return render(request, 'store/allTopSellingsMovies.html', context)

def newReleasesmovies(request):
    today = datetime.datetime.now()
    current_year = today.year
    last_year = current_year - 1
    
    newReleases = Movie.objects.filter(Q(Date__year=current_year) | Q(Date__year = last_year))

    context = {"newReleases" : newReleases}
    return render(request, 'store/allNewReleasesMovies.html', context)

def moviesRecommendations(request):
    return render(request, 'store/allMoviesRecommendations.html')
    

def movieItem(request , movie_id):
    movie = Movie.objects.get(id=movie_id)
    if request.method == "POST":
        if 'currency' in request.POST:
            currency = request.POST.get('currency')
        else:
            if 'like' in request.POST:
                like = request.POST.get('like')
                review = Review.objects.get(id=like)
                review.likes += 1
                review.save()
            elif 'dislike' in request.POST:
                dislike = request.POST.get('dislike')
                review = Review.objects.get(id=dislike)
                review.dislikes += 1
                review.save()
            elif 'report' in request.POST:
                report = request.POST.get('report')
                review = Review.objects.get(id=report)
                review.report += 1
                if review.report >= 10:
                    review.delete()   
        
    try:
        reviews = Review.objects.filter(movie_id=movie)
        currency = "USD"
        similarMovies = Movie.objects.filter(Genre = movie.Genre)
        cast = CastMember.objects.filter(Movie=movie)
        credit = CreditMemeber.objects.filter(Movie= movie)
        average_rating = 0
        if reviews:
            for review in reviews:
                average_rating += review.Rating
            average_rating = average_rating/reviews.__len__()
        else:
            average_rating = 0
    except movie.DoesNotExist:
        return render(request, 'store/error.html')
    
    context = {"movie" : movie,
                "similarMovies" : similarMovies,
                "cast" : cast,
                "credit": credit,
                "reviews": reviews ,
                "average": average_rating,
                "currency" : currency
                }
    print(currency)
    return render(request, 'store/selectedMovie.html', context)



def wishlist(request):
    wishlist = WishList.objects.all()
    context = {"wishlist" : wishlist}
    return render(request, 'store/wishlist.html', context)