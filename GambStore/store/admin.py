from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Game, Movie, Application, Book, CreditMemeber, CastMember, Profile, Review , WishList


admin.site.register(Game)
admin.site.register(Movie)
admin.site.register(Application)
admin.site.register(Book)
admin.site.register(CreditMemeber)
admin.site.register(CastMember)
admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(WishList)