from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('terms/', views.termOfServices, name='terms'),
    path('error/', views.error, name='error'),
    # path('testitem/' , views.item , name='itemtest'),

    path('bookItem/<int:book_id>/', views.bookItem, name='bookItem'),
    path('gameItem/<int:game_id>/', views.gameItem, name='gameItem'),
    path('appItem/<int:app_id>/', views.applicationItem, name='appItem'),
    path('movieItem/<int:movie_id>/', views.movieItem, name='movieItem'),

    path('bookCategory/', views.bookCategory, name='bookCategory'),
    path('movieCategory/', views.movieCategory, name='movieCategory'),
    path('gameCategory/', views.gameCategory, name='gameCategory'),
    path('applicationCategory/', views.applicationCategory, name='applicationCategory'),

    path('topSellingBooks/', views.topSellingBooks, name='topSellingBooks'),
    path('newReleasesBooks/', views.newReleasesBooks, name='newReleasesBooks'),
    path('booksRecommendations', views.booksRecommendations, name='booksRecommendations'),

    path('topSellingGames/', views.topSellingGames, name='topSellingGames'),
    path('newReleasesGames/', views.newReleasesGames, name='newReleasesGames'),
    path('gamesRecommendations', views.gamesRecommendations, name='gamesRecommendations'),

    path('topSellingmovies/', views.topSellingmovies, name='topSellingmovies'),
    path('newReleasesmovies/', views.newReleasesmovies, name='newReleasesmovies'),
    path('moviesRecommendations', views.moviesRecommendations, name='moviesRecommendations'),

    path('topSellingApplications/', views.topSellingApplications, name='topSellingApplications'),
    path('newReleasesApplications/', views.newReleasesApplications, name='newReleasesApplications'),
    path('applicationsRecommendations', views.applicationsRecommendations, name='applicationsRecommendations'),
    
    path('wishlist/', views.wishlist, name='wishlist'),
    path('search/', views.search, name='search'),
    path('visitedItems/', views.visitedItems, name='visitedItems')
]