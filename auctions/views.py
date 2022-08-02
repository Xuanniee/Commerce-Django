import re
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from decimal import *

from .models import Auction_Listing, User, Bid, Comment, WatchList
from .forms import NewListing, CommentForm
from .categories import COMMERCE_CATEGORIES

def index(request):
    # Render HTML with Context
    return render(request, "auctions/index.html", {
        "listings": Auction_Listing.objects.filter(active=True)
    })

def inactive(request):
    return render(request, "auctions/inactive.html",{
        "listings": Auction_Listing.objects.filter(active=False)
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)

        # Create an Empty Watchlist for the User
        user_watchlist = WatchList.objects.create(user=user)
        user_watchlist.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# Create New Listing
def create_listing(request):
    # Create a New Listing through POST
    if request.method == "POST":
        # Get User Input
        listing_title = request.POST["title"]
        listing_des = request.POST["description"]
        listing_start_bid = Decimal(request.POST["starting_bid"])
        listing_category = request.POST["category"] 
        listing_url = request.POST["image_url"]

        # Adding a New Listing
        current_user = request.user
        new_listing = Auction_Listing(auction_title=listing_title, auction_description=listing_des, auction_bid=listing_start_bid, auction_category=listing_category, auction_opt_img=listing_url, user=current_user)
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))

    # GET Request
    else:
        return render(request, "auctions/new_listing.html", {
            # Pass in the Django Form
            'form': NewListing()
        })

# Listing Function
def listing(request, listing_id):
    # Getting the Identity of the Visitor who is Logged in
    current_user = request.user
    requested_listing = Auction_Listing.objects.get(pk=listing_id)

    # POST Request
    if request.method == "POST":

        # Comment was submitted
        if request.POST.get("Comment-Button") == "Comment":
            # Comment was made
            comment_form = CommentForm(request.POST or None)
            # Form Validation
            if comment_form.is_valid():
                # Get the User Comment
                comment_content = request.POST.get('comment_area')
                # Create a Comment Object but not saved to Database yet
                new_user_comment = Comment.objects.create(comment=comment_content, user=current_user, listing=requested_listing)
                # Save it to our Database
                new_user_comment.save()
                # Comment Success
                messages.add_message(request, messages.INFO, "Comment posted!!")
            else:
                # Tell User about Error before Redirecting them
                messages.add_message(request, messages.WARNING, "Comment was unable to be posted!!")
            
            # Redirect the User to the Listing with the New Comment
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))


        # Bid Button was pressed
        elif request.POST.get("Bid-Button") == "Bid":
            # Bid was made
            # Request.POST is a Query Dict: {'csrfmiddlewaretoken': ['aHmkjwhr5243rU2g6VfWUEnhOsYNlaFuZhCoIGqcSxQJuVgBeYKKjMpuxTxUyeyk'], 'Bid-Value': ['110'], 'Bid-Button': ['Bid']}
            user_bid_value = Decimal(request.POST['Bid-Value'])
            current_bid = requested_listing.auction_bid

            if user_bid_value > current_bid:
                # Updating the Bid iif the new Bid is Larger
                requested_listing.auction_bid = user_bid_value # Assign
                requested_listing.save() # Saving Record

                # Record the Transaction in Bid Model
                new_bid_record = Bid(bidding_price=user_bid_value, user=current_user, listing=requested_listing)
                new_bid_record.save()

                # Inform User Bid was made
                messages.add_message(request, messages.SUCCESS, "Bid has been placed!!")
            
            # If Bid is smaller
            else:
                # Inform the User the Bid Cannot be Made
                messages.add_message(request, messages.WARNING, "Bid was unsuccessful as the bid was too small. Please try again!!")

        
        # End Auction Button was pressed
        elif request.POST.get('End_Auction_Button') == 'End_Auction':
            
            # Update the Active Status of Listing
            requested_listing.active = False
            # Save the Record into Database
            requested_listing.save()
            # Inform User Auction was closed successfully
            messages.add_message(request, messages.SUCCESS, "Auction has been closed successfully. Congratualations!!")
            # Redirect User to Non-Active Listings
            return HttpResponseRedirect(reverse("index"))
            

        # Redirect User back to Listing
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    
    else:
        # Use Listing ID to retrieve the other properties from Django Models
        requested_listing = Auction_Listing.objects.get(pk=listing_id)
        current_user = request.user
        listing_comments = Comment.objects.filter(listing=requested_listing)
        bids_for_listing = Bid.objects.filter(listing=listing_id)
        number_of_bids = bids_for_listing.count()

        # Iterate through all the Bids made
        for bid in bids_for_listing:
            # Find Highest bidder
            if bid.bidding_price == requested_listing.auction_bid:
                current_highest_bidder = bid.user
        
        # Starting Bid
        if number_of_bids == 0:
            current_highest_bidder = "No One"

        # Watchlist
        current_user_watchlist = (WatchList.objects.filter(user=current_user))[0]
        listings_in_watchlist = current_user_watchlist.listing.all()

        # Check if Listing is already in User's Watchlist
        if listings_in_watchlist.filter(listing_id=listing_id).exists():
            # Present
            listing_in_watchlist = True
        else:
            # Not Present
            listing_in_watchlist = False

        return render(request, "auctions/listing.html",{
            'listing': requested_listing,
            'comment_box': CommentForm(),
            'listing_comments': listing_comments,
            'current_user': current_user,
            'bid_count': number_of_bids,
            'highest_bidder': current_highest_bidder,
            'watchlist_listings': listings_in_watchlist,
            "in_watchlist": listing_in_watchlist
        })

# Watchlist View
def watchlist(request, user_id):
    current_user = request.user # User
    

    if request.method == "POST":
        # Get Listing ID as I can't pass it as an argument
        listing_id = request.POST.get('listing-id')

        # Add to Watchlist
        if request.POST.get('Add_Watchlist_Button') == 'Add_Watchlist':
            # Item/Listing to be saved
            listing_to_be_saved = get_object_or_404(Auction_Listing, listing_id=listing_id) # Listing
            
            # Check if Listing is already present in Watchlist
            if WatchList.objects.filter(user=current_user, listing=listing_to_be_saved).exists():
                messages.add_message(request, messages.WARNING, 'Could not be added. This listing is already present in your watchlist!!')   
                # Redirect User to Listing
                return HttpResponseRedirect(reverse("watchlist", args=[current_user.user_id]))            

            # Get User Watchlist or Create if it doesn't exists (Method returns a Tuple)
            user_watchlist, created = WatchList.objects.get_or_create(user=current_user)

            # Save the Current Updated Watchlist Properties
            user_watchlist.save()

            # Cannot assign a ManyToMany field directly like get_or_create above; Need to use .add() or .set() --> Removes Duplicates
            # Save the Many to Many Field
            user_watchlist.listing.add(listing_to_be_saved)

            # Notify User when Item is added
            messages.add_message(request, messages.INFO, 'Listing added to your Watchlist successfully!!')           # Seen in Django Admin only. Not very helpful

            # Redirect User to their Watchlist
            return HttpResponseRedirect(reverse("watchlist", args=[current_user.user_id]))
        
        elif request.POST.get('Remove_Watchlist_Button') == 'Remove_Watchlist': 
            # Listing to be removed
            listing_to_be_removed = get_object_or_404(Auction_Listing, listing_id=listing_id) # Listing

            # Ensure Listing is in Watchlist
            if not WatchList.objects.filter(user=current_user, listing=listing_to_be_removed).exists():
                print(request)
                #messages.info(request, "Could not be removed. This listing is not present in your watchlist!!")
                messages.add_message(request, messages.WARNING, 'Could not be removed. This listing is not present in your watchlist!!')   
                # Redirect User to Listing
                return HttpResponseRedirect(reverse("watchlist", args=[current_user.user_id]))
            
            # Get User Watchlist or Create if it doesn't exists (Method returns a Tuple)    
            user_watchlist, created = WatchList.objects.get_or_create(user=current_user)            # Created is a Boolean
            
            # Save the Current Updated Watchlist Properties
            user_watchlist.save()

            # Remove from Watchlist
            user_watchlist.listing.remove(listing_to_be_removed)

            # Notify User when Item is added
            print(request)
            messages.add_message(request, messages.INFO, 'Listing removed from your watchlist successfully!!')

            # Redirect User to their Watchlist
            return HttpResponseRedirect(reverse("watchlist", args=[current_user.user_id]))

    # GET Request
    else:
        # Get User's Watchlist
        current_user_watchlist = (WatchList.objects.filter(user=current_user))[0]
        
        # Check if there are listings inside of the User's Watchlist
        if current_user_watchlist.listing.count() == 0:
            empty_watchlist = True
        else:
            empty_watchlist = False
                
        # Render the User Watchlist
        return render(request, "auctions/watchlist.html",{
            "user": current_user,
            "listings": current_user_watchlist.listing.all(),
            "empty_watchlist": empty_watchlist
        })

# Categories
def categories(request):
    # Filtered Categories via POST
    if request.method == "POST":
        # Get the Category requested by User
        requested_category = request.POST.get("filtered_category").upper()

        # Get all the Listings in the relevant Category
        listings_in_category = Auction_Listing.objects.filter(active=True, auction_category=requested_category)

        # Check if the Filter is Empty
        if listings_in_category.exists() :
            empty_category = False
        else:
            empty_category = True

        return render(request, "auctions/categories.html", {
            "category": requested_category,
            "listings": listings_in_category,
            "empty_category": empty_category
        })


    # GET Request
    else:
        return render(request, "auctions/categories.html", {
            "categories": COMMERCE_CATEGORIES
        })