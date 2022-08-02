from django.contrib.auth.models import AbstractUser
from django.db import models

from .categories import COMMERCE_CATEGORIES


class User(AbstractUser):
    # Inherits from Django's AbstractUser
    user_id = models.BigAutoField(primary_key=True)
    pass
    # No 2 User should have identical usernames
    # username = models.CharField(max_length=150, unique=True)
    # email = models.EmailField(unique=True)
    # password = models.CharField(max_length=200)
    # USERNAME_FIELD = 'username'
    # # Username Field must not be in Required Fields
    # REQUIRED_FIELDS = ['email', 'password']

    # # String Representation
    # def __str__(self):
    #     return f"User {self.user_id}'s Details:\
    #              Username: {self.username}\
    #              Email: {self.email}\
    #              Password Hash: {self.password}"

# Django Model for Auction Listings (Will Make Main Table for NOW)
class Auction_Listing(models.Model):
    listing_id = models.AutoField(primary_key=True)
    # Properties of Auction Listings to be tracked
    auction_title = models.CharField(max_length=64)
    auction_description = models.TextField()
    # Max Digits is Arbitrary Number
    auction_bid = models.DecimalField(max_digits=20, decimal_places=2)
    auction_category = models.CharField(choices=COMMERCE_CATEGORIES, max_length=64)
    auction_opt_img = models.URLField(max_length=1000)
    active = models.BooleanField(default=True, null=True, blank=True)

    # Many-to-One Relationship with User
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Listing_Owner", null=True, blank=True)

    # String Representation of Auction Listing
    # def __str__(self):
    #     return f"Listing Id: {self.listing_id}; Title: {self.auction_title};  Current Price: {self.auction_bid};  Description: {self.auction_description}"

# Bids
class Bid(models.Model):
    # Necessary Properties
    bidding_id = models.BigAutoField(primary_key=True)
    bidding_price = models.DecimalField(max_digits=20, decimal_places=2)
    # Many to One Relationship with User & Listing
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bidder")
    listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="Listing", null=True, blank=True)

# Comments
class Comment(models.Model):
    # Necessary Properties
    comment_id = models.BigAutoField(primary_key=True)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    # Also Many to One Relationship with User as each User can make multiple bids, comments, listings
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Commentor", null=True, blank=True)
    listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="Listing_Comments", null=True, blank=True)

    # Metadata for the Comments Model
    class Meta:
        ordering = ['created']

    def __str__(self):
        if not self.user:
            return "Anonymous"
        return f"Comment by {self.user.username} on {self.listing}"

# Watchlist
class WatchList(models.Model):
    watchlist_id = models.BigAutoField(primary_key=True)
    # One to One Relationship with User
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Watchlist_Owner", null=True, blank=True)
    # Many to Many Relationship with Listing (Users can have multiple products in Watchlist. A Product can be in multiple Watchlists at any one time)
    listing = models.ManyToManyField(Auction_Listing, related_name="Watchlisted_Listing", blank=True)

    def __str__(self):
        return f"{self.user}'s Watchlist"