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
    Name         = models.CharField(max_length=120)
    Genre        = models.CharField(max_length=120)
    Rating       = models.IntegerField()
    Date         = models.DateField()
    CopiesSold   = models.IntegerField()
    Price        = models.BigIntegerField()
    Image        = models.ImageField(upload_to="Static/store/books", null=True, blank=True)
    Image1       = models.ImageField(upload_to="Static/store/books", null=True, blank=True)
    Image2       = models.ImageField(upload_to="Static/store/books", null=True, blank=True)
    Image3       = models.ImageField(upload_to="Static/store/books", null=True, blank=True)
    Description  = models.TextField()
    CreatedAt    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Name

class Application(models.Model):
    Name         = models.CharField(max_length=120)
    Genre        = models.CharField(max_length=120)
    Rating       = models.IntegerField()
    Date         = models.DateField()
    CopiesSold   = models.IntegerField()
    Price        = models.BigIntegerField()
    Image        = models.ImageField(upload_to="Static/store/applications", null=True, blank=True)
    Image1       = models.ImageField(upload_to="Static/store/applications", null=True, blank=True)
    Image2       = models.ImageField(upload_to="Static/store/applications", null=True, blank=True)
    Image3       = models.ImageField(upload_to="Static/store/applications", null=True, blank=True)
    Description  = models.TextField()
    CreatedAt    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Name

class Game(models.Model):
    Name         = models.CharField(max_length=120)
    Genre        = models.CharField(max_length=120)
    Rating       = models.IntegerField()
    Date         = models.DateField()
    CopiesSold   = models.IntegerField()
    Price        = models.BigIntegerField()
    Image        = models.ImageField(upload_to="Static/store/games", null=True, blank=True)
    Image1       = models.ImageField(upload_to="Static/store/games", null=True, blank=True)
    Image2       = models.ImageField(upload_to="Static/store/games", null=True, blank=True)
    Image3       = models.ImageField(upload_to="Static/store/games", null=True, blank=True)
    Description  = models.TextField()
    CreatedAt    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Name

class Movie(models.Model):
    Name         = models.CharField(max_length=120)
    Genre        = models.CharField(max_length=120)
    Rating       = models.IntegerField()
    Date         = models.DateField()
    CopiesSold   = models.IntegerField()
    Price        = models.BigIntegerField()
    Image        = models.ImageField(upload_to="Static/store/movies", null=True, blank=True)
    Image1       = models.ImageField(upload_to="Static/store/movies", null=True, blank=True)
    Image2       = models.ImageField(upload_to="Static/store/movies", null=True, blank=True)
    Image3       = models.ImageField(upload_to="Static/store/movies", null=True, blank=True)
    Trailer      = models.CharField(max_length=255)
    Description  = models.TextField()
    CreatedAt    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Name

class CastMember(models.Model):
    Name        = models.CharField(max_length=120)
    Movie       = models.ForeignKey(Movie, on_delete=models.CASCADE)

class CreditMemeber(models.Model):
    Name        = models.CharField(max_length=120)
    Job         = models.CharField(max_length=120)
    Movie       = models.ForeignKey(Movie, on_delete=models.CASCADE)

class Review(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id        = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    movie_id       = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    game_id        = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)
    application_id = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True)
    likes          = models.IntegerField(null=True)
    dislikes       = models.IntegerField(null=True)
    content        = models.TextField()
    report         = models.IntegerField(null=True)
    Rating         = models.IntegerField()


class WishList(models.Model):
    user              = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id           = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    movie_id          = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    application_id    = models.ForeignKey(Application, on_delete=models.CASCADE, null=True)
    game_id           = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)


class VisitedItems(models.Model):
    user              = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book_id           = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    movie_id          = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    application_id    = models.ForeignKey(Application, on_delete=models.CASCADE, null=True)
    game_id           = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)