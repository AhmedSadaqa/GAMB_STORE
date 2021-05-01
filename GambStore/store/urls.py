from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('terms/', views.termOfServices, name='terms'),
    path('testitem/' , views.item , name='itemtest'),
    path('bookItem/<int:book_id>/', views.bookItem, name='bookItem'),
    path('bookCategory/', views.bookCategory, name='bookCategory'),
    path('bookCategory/topSellings', views.topSellingBooks, name='topSellingBooks'),
    path('bookCategory/newReleases', views.newReleases, name='newReleases'),
    path('bookCategory/recommendations', views.recommendations, name='recommendations'),
]