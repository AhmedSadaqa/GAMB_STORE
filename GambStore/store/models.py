from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from decimal import Decimal
from django.contrib.auth.models import User

class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    Image       = models.ImageField(default="defaultPic.png", upload_to="profile_pics")

class Book(models.Model):
    Name        = models.CharField(max_length=120)
    Genre       = models.CharField(max_length=120)
    Rating      = models.IntegerField()
    Date        = models.DateTimeField()
    CopiesSold  = models.IntegerField()
    Price       = models.DecimalField(max_digits=5, decimal_places=2)
    Image       = models.ImageField(upload_to="Static/store/books", null=True, blank=True)
    Description = models.TextField()
    CreatedAt   = models.DateTimeField(auto_now=True)

class Application(models.Model):
    Name        = models.CharField(max_length=120)
    Genre       = models.CharField(max_length=120)
    Rating      = models.IntegerField()
    Date        = models.DateTimeField()
    CopiesSold  = models.IntegerField()
    Price       = models.DecimalField(max_digits=5, decimal_places=2)
    Image       = models.ImageField(upload_to="Static/store/applications", null=True, blank=True)
    Description = models.TextField()
    CreatedAt   = models.DateTimeField(auto_now=True)

class Game(models.Model):
    Name        = models.CharField(max_length=120)
    Genre       = models.CharField(max_length=120)
    Rating      = models.IntegerField()
    Date        = models.DateTimeField()
    CopiesSold  = models.IntegerField()
    Price       = models.DecimalField(max_digits=5, decimal_places=2)
    Image       = models.ImageField(upload_to="Static/store/games", null=True, blank=True)
    Description = models.TextField()
    CreatedAt   = models.DateTimeField(auto_now=True)

class Movie(models.Model):
    Name        = models.CharField(max_length=120)
    Genre       = models.CharField(max_length=120)
    Rating      = models.IntegerField()
    Date        = models.DateTimeField()
    CopiesSold  = models.IntegerField()
    Price       = models.DecimalField(max_digits=5, decimal_places=2)
    Image       = models.ImageField(upload_to="Static/store/movies", null=True, blank=True)
    Trailer     = models.FileField()
    Description = models.TextField()
    CreatedAt   = models.DateTimeField(auto_now=True)

class CastMember(models.Model):
    Name        = models.CharField(max_length=120)
    Movie       = models.ForeignKey(Movie, on_delete=models.CASCADE)

class CreditMemeber(models.Model):
    Name        = models.CharField(max_length=120)
    Job         = models.CharField(max_length=120)
    Movie       = models.ForeignKey(Movie, on_delete=models.CASCADE)

class Review(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    Book       = models.ForeignKey(Book, on_delete=models.CASCADE)
    Movie      = models.ForeignKey(Movie, on_delete=models.CASCADE)
    Game       = models.ForeignKey(Game, on_delete=models.CASCADE)
    Application= models.ForeignKey(Application, on_delete=models.CASCADE)