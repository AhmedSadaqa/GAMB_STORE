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
    context = {"books":books,
               "applications":applications,
               "games":games,
               "movies":movies}
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
    for i in range(10):
        tenTopSellingBooks.append(topSellingbooks[i])
        
    # New Releases Books
    today = datetime.datetime.now()
    current_year = today.year
    last_year = current_year - 1
    
    newReleasesBooks = Book.objects.filter(Q(Date__year=current_year) | Q(Date__year = last_year))
    tenNewReleasesBooks = []
    for i in range(10):
        tenNewReleasesBooks.append(newReleasesBooks[i])

    
    #Recommendations
    Recommendations = Book.objects.filter(Rating__gte=7)
    tenRecommendations = []
    for i in range(10):
        tenRecommendations.append(Recommendations[i])

    context = {"tenTopSellingBooks" : tenTopSellingBooks,
               "tenNewReleasesBooks": tenNewReleasesBooks,
               "tenRecommendations" : tenRecommendations     
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
    Recommendations = Book.objects.filter(Rating__gte=7)
    context = {"Recommendations" : Recommendations}
    return render(request, 'store/allBooksRecommendations.html', context)


def bookItem(request, book_id):
    current_user = request.user
    book = Book.objects.get(id=book_id)
    itemVisited = VisitedItems.objects.create(user=current_user,
                                              book_id=book)
    books = Book.objects.get(id=book_id)
    if request.method == "POST":
        if 'currency' in request.POST:
            currency = request.POST.get('currency')
        elif 'wishlist' in request.POST:
            count = WishList.objects.filter(book_id=book).count()
            if count == 0:
                wishlist = WishList.objects.create(user= request.user,
                                               book_id= book)
        else:
            if 'review' in request.POST:
                review_content = request.POST.get('rev')
                review_user = request.user
                review_rating = request.POST.get('rating')
                Review.objects.create(user=review_user , Rating=review_rating, book_id=books, likes=0, dislikes=0, report=0, content=review_content)
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
    if request.method == "POST":
        filtering = request.POST.get("filter")
        filteredApps = Application.objects.filter(Genre=filtering)
        return render(request, 'store/filteredApps.html', {'filteredApps' : filteredApps, 'filtering' : filtering})

    #Top Selling
    topSellingApps = Application.objects.all().order_by("-CopiesSold")
    tenTopSellingApps = []
    for i in range(10):
        tenTopSellingApps.append(topSellingApps[i])

    #New Releases
    today = datetime.datetime.now()
    current_year = today.year
    last_year = current_year - 1

    newReleasesApps = Application.objects.filter(Q(Date__year=current_year) | Q(Date__year=last_year))
    tenNewReleasesApps = []
    print(newReleasesApps)
    for i in range(3):
        tenNewReleasesApps.append(newReleasesApps[i])

    #Recommendations
    Recommendations = Application.objects.filter(Rating__gte=7)
    tenRecommendations = []
    for i in range(10):
        tenRecommendations.append(Recommendations[i])
    
    context = {"tenTopSellingApps" : tenTopSellingApps,
               "tenNewReleasesApps" : tenNewReleasesApps,
               "tenRecommendations" : tenRecommendations}
    

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
    Recommendations = Application.objects.filter(Rating__gte=7)
    context = {"Recommendations" : Recommendations}
    return render(request, 'store/allAppsRecommendations.html', context)

def applicationItem(request , app_id):
    current_user = request.user
    app = Application.objects.get(id=app_id)
    itemVisited = VisitedItems.objects.create(user=current_user,
                                              application_id=app)
    app = Application.objects.get(id=app_id)
    if request.method == "POST":
        if 'currency' in request.POST:
            currency = request.POST.get('currency')
        elif 'wishlist' in request.POST:
            count = WishList.objects.filter(application_id=app).count()
            if count == 0:
                wishlist = WishList.objects.create(user= request.user,
                                               application_id= app)

        else:
            if 'review' in request.POST:
                review_content = request.POST.get('rev')
                review_user = request.user
                review_rating = request.POST.get('rating')
                Review.objects.create(user=review_user , Rating=review_rating, game_id=game, likes=0, dislikes=0, report=0, content=review_content)
            elif 'like' in request.POST:
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
    if request.method == "POST":
        filtering = request.POST.get("filter")
        filteredGames = Game.objects.filter(Genre=filtering)
        return render(request, 'store/filteredGames.html', {'filteredGames' : filteredGames, 'filtering' : filtering})
    
    #Top Selling
    topSellingGames = Game.objects.all().order_by('-CopiesSold')
    tenTopSellingGames = []
    for i in range(10):
        tenTopSellingGames.append(topSellingGames[i])
    
    #New Releases Games
    today = datetime.datetime.now()
    current_year = today.year
    last_year = current_year - 1

    newReleasesGames = Game.objects.filter(Q(Date__year=current_year) | Q(Date__year=last_year))
    tenNewReleasesGames = []
    for i in range(5):
        tenNewReleasesGames.append(newReleasesGames[i])
    
    #Recommendations
    Recommendations = Game.objects.filter(Rating__gte=7)
    print(Recommendations)
    tenRecommendations = []
    for i in range(10):
        tenRecommendations.append(Recommendations[i])
    

    context = {"tenTopSellingGames" : tenTopSellingGames,
               "tenNewReleasesGames": tenNewReleasesGames,
               "tenRecommendations" : tenRecommendations} 
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
    Recommendations = Game.objects.filter(Rating__gte=7)
    context = {"Recommendations" : Recommendations}
    return render(request, 'store/allGamesRecommendations.html', context)

def gameItem(request , game_id):
    current_user = request.user
    game = Game.objects.get(id=game_id)
    itemVisited = VisitedItems.objects.create(user=current_user,
                                              game_id=game)
    game = Game.objects.get(id=game_id)
    if request.method == "POST":
        if 'currency' in request.POST:
            currency = request.POST.get('currency')
        elif 'wishlist' in request.POST:
            count = WishList.objects.filter(game_id=game).count()
            if(count == 0):
                wishlist = WishList.objects.create(user= request.user,
                                               game_id= game)
        else:
            if 'review' in request.POST:
                review_content = request.POST.get('rev')
                review_user = request.user
                review_rating = request.POST.get('rating')
                Review.objects.create(user=review_user , Rating=review_rating, game_id=game, likes=0, dislikes=0, report=0, content=review_content)
            elif 'like' in request.POST:
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
    return render(request, 'store/selectedGame.html', context)

# MOVIES

def movieCategory(request):
    if request.method == "POST":
        filtering = request.POST.get("filter")
        filteredMovies = Movie.objects.filter(Genre=filtering)
        return render(request, 'store/filteredMovies.html', {'filteredMovies' : filteredMovies, 'filtering' : filtering})
    
    #Top Sellings
    topSellingMovies = Movie.objects.all().order_by("-CopiesSold")
    tenTopSellingMovies = []
    for i in range(10):
        tenTopSellingMovies.append(topSellingMovies[i])
    
    #New Releases
    today = datetime.datetime.now()
    current_year = today.year
    last_year = current_year - 1

    newReleasesMovies = Movie.objects.filter(Q(Date__year=current_year) | Q(Date__year=last_year))
    tenNewReleasesMovies = []
    for i in range(10):
        tenNewReleasesMovies.append(newReleasesMovies[i])
    
    #Recommendations
    Recommendations = Movie.objects.filter(Rating__gte=7)
    print(Recommendations)
    tenRecommendations = []
    for i in range(10):
        tenRecommendations.append(Recommendations[i])
    
    context = {"tenTopSellingMovies" : tenTopSellingMovies,
               "tenNewReleasesMovies": tenNewReleasesMovies,
               "tenRecommendations" : tenRecommendations     
            }
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
    Recommendations = Movie.objects.filter(Rating__gte=7)
    context = {"Recommendations" : Recommendations}
    return render(request, 'store/allMoviesRecommendations.html', context)
    

def movieItem(request , movie_id):
    current_user = request.user
    movie = Movie.objects.get(id=movie_id)
    itemVisited = VisitedItems.objects.create(user=current_user,
                                              movie_id=movie)
    if request.method == "POST":
        if 'currency' in request.POST:
            currency = request.POST.get('currency')
        elif 'wishlist' in request.POST:
            count = WishList.objects.filter(movie_id=movie).count()
            if(count == 0):
                wishlist = WishList.objects.create(user= request.user,
                                               movie_id= movie)
        else:
            if 'review' in request.POST:
                review_content = request.POST.get('rev')
                review_user = request.user
                review_rating = request.POST.get('rating')
                Review.objects.create(user=review_user , Rating=review_rating, movie_id=movie, likes=0, dislikes=0, report=0, content=review_content)
            elif 'like' in request.POST:
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
    return render(request, 'store/selectedMovie.html', context)




    #WishList & Search Options
def wishlist(request):
    wishlist = WishList.objects.distinct()
    print(wishlist)
    context = {"wishlist" : wishlist}
    return render(request, 'store/wishlist.html', context)


def search(request):
    result = request.GET.get("q")
    booksResult = Book.objects.filter(Q(Name=result) | Q(Description__icontains=result))
    moviesResult = Movie.objects.filter(Q(Name=result) | Q(Description__icontains=result))
    appsResult = Application.objects.filter(Q(Name=result) | Q(Description__icontains=result))
    gamesResult = Game.objects.filter(Q(Name=result) | Q(Description__icontains=result))


    if request.method == "POST":
        filterResult = request.POST.get("filter")
        if filterResult == "Book":
            return render(request, 'store/base.html', {"booksResult" :booksResult })
        elif filterResult == "Application":
            return render(request, 'store/base.html', {"appsResult" : appsResult})
        elif filterResult == "Game":
            return render(request, 'store/base.html', {"gamesResult" : gamesResult})
        else:
            return render(request, 'store/base.html', {"moviesResult" : moviesResult})

    context = {"booksResult" : booksResult,
               "moviesResult" : moviesResult,
               "appsResult" : appsResult,
               "gamesResult" : gamesResult,
               }

    return render(request, 'store/base.html', context)

def visitedItems(request):
    items = VisitedItems.objects.all().order_by("-id")
    lastVisited = []
    for i in range(24):
        lastVisited.append(items[i])
    context = {"lastVisited" : lastVisited}
    return render(request, 'store/visitedItems.html', context)



def addReviews(request, rating):
    movies = Movie.objects.all()
    books = Book.objects.all()
    apps = Application.objects.all()
    games = Game.objects.all()

    review = "The website is a great source for affordable books and movies. I have shopped through the website for a few years now and am always pleased. If there is a problem, it is resolved quickly and satisfactorily. I plan to continue to buy books from this site regularly. "

    count = 0

    for movie in movies:
        if count >= 6:
            Review.objects.create(user=request.user , movie_id=movie, Rating=rating , content=review, likes=0, dislikes=0, report=0)
        count += 1

    for book in books:
        if count >= 6:
            Review.objects.create(user=request.user , book_id=book, Rating=rating , content=review, likes=0, dislikes=0, report=0)
        count += 1

    for app in apps:
        if count >= 6:
            Review.objects.create(user=request.user , application_id=app, Rating=rating , content=review, likes=0, dislikes=0, report=0)
        count += 1

    for game in games:
        if count >= 6:
            Review.objects.create(user=request.user , game_id=game, Rating=rating , content=review, likes=0, dislikes=0, report=0)
        count += 1

    context = {"books":books,
               "applications":apps,
               "games":games,
               "movies":movies}
    return render(request, "store/GAMBindex.html", context)