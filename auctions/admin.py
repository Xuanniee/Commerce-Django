from django.contrib import admin
from .models import Auction_Listing, Bid, Comment, User, WatchList

# Register your models here.
admin.site.register(User)
admin.site.register(Auction_Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(WatchList)