from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='store-home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('terms/', views.termOfServices, name='terms'),
    path('testitem/' , views.item , name='itemtest')
]