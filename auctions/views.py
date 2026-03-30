from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import BidForm,CommentsForm
from .models import User
from .models import ListingCategories, Listings, ListingComments, ListingBids, WhatchList
from django.contrib import messages

# Active Listings index page
def index(request):
 
    activeListings = Listings.objects.filter(status="T")
    for activeListing in activeListings:
        latest_bid = activeListing.listing_bids.order_by('-id').first()
       
        if latest_bid:
            activeListing.latest_bid = latest_bid.bid
        else:
            activeListing.latest_bid = "N/A"
    

    return render(request, "auctions/index.html",{
        "activeListings":activeListings,
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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# Single listing page
def listing(request,listname):
    # listings = Listing.ob
    listing = Listings.objects.get(title=listname)
    listingbids = listing.listing_bids.all()
    latest_bid =""
    comments = listing.listing_comments.all()
    bidForm = BidForm()
    commentForm = CommentsForm()
    listingowner = ""
    listingwinner =""
    exists= False
  
 
    if request.user.is_authenticated:
         # check if the user is the listing owner
        if request.user == listing.user:
            listingowner = listing.user

        # check if the user is the listing winner
        if request.user.username == listing.winner:
            listingwinner = listing.winner

                
        if WhatchList.objects.filter(user=request.user,listing=listing).exists():
            exists = True
            

        else:
            exists = False

        if request.method == "POST":
            if 'submit_bid' in request.POST:
                bidForm= BidForm(request.POST)
                if  bidForm.is_valid():
                    data_valid = bidForm.cleaned_data
                    if data_valid["bid"] > listing.starting_price:
                        if not listingbids or data_valid["bid"] > listingbids.order_by('-bid').first().bid:
                            bid =  ListingBids(user=request.user,listing=listing,bid=data_valid["bid"])
                            bid.save()
                            messages.success(request, "You have successfuly placed your bid.")
                            return HttpResponseRedirect(reverse("listing" ,args=[listing.title]))
                        else:
                            bidForm.add_error("bid","Error: A bid must be greater than the latest bid.")
                    else:
                        bidForm.add_error("bid","Error: A bid must be greater than the starting bid.")
   
            if 'submit_comment' in request.POST:
                commentForm = CommentsForm(request.POST)
                if  commentForm.is_valid():
                    validCommentData = commentForm.cleaned_data
                    comment = ListingComments(user=request.user,listing=listing,content=validCommentData["comment"])
                    comment.save()
                    return HttpResponseRedirect(reverse("listing" ,args=[listing.title]))

            if 'listing_status_submit' in request.POST:
                if listingbids:
                    listing.status = "F"
                    highestbiduser=listingbids.order_by('-bid').first().user.username
                    listing.winner = highestbiduser
                    listing.save()
                    messages.success(request, "You have successfuly closed the listing.")
                    
                else:
                    messages.error(request, "The listing has no active bids.")
                    # return HttpResponseRedirect(reverse("listing" ,args=[listing.title]))


                return HttpResponseRedirect(reverse("listing" ,args=[listing.title]))

            if 'add_watchlist' in request.POST:
                watchlistrecord = WhatchList(user=request.user,listing=listing)
                watchlistrecord.save()
                messages.success(request, "You have successfuly added the listing in your watchlist.",extra_tags="watchlist")
                return HttpResponseRedirect(reverse("listing" ,args=[listing.title]))

            if 'remove_watchlist' in request.POST:
                watchlist_item = WhatchList.objects.filter(user=request.user,listing=listing).get()
                watchlist_item.delete()

                messages.success(request, "You have successfuly deleted the listing from your watchlist.",extra_tags="watchlist")
                return HttpResponseRedirect(reverse("listing" ,args=[listing.title]))

       

    if listingbids:
        latest_bid = listingbids.order_by('-bid').first().bid


        


    return render(request, "auctions/listing.html",{
        "bidForm": bidForm,
        "latest_bid": latest_bid,
        "listing": listing,
        "commentForm":commentForm,
        "comments":comments,
        "listingowner":listingowner,
        "listingwinner":listingwinner,
        "exists":exists,
    })

# Listing categories
def categories(request):
    categories = ListingCategories.objects.all()
    return render(request, "auctions/categories.html",{
        "categories": categories
    })

# Single Category page
def category(request,catname):
    categories = ListingCategories.objects.all()
    category = categories.get(name=catname)
    listings = category.category_listings.all()
    return render(request, "auctions/category.html",{
        "category": category,
        "listings": listings,
    })

@login_required
def watchlist(request):
    watchlist_items = WhatchList.objects.filter(user=request.user)
    for watchlist_item in watchlist_items:
        latest_bid = watchlist_item.listing.listing_bids.order_by('-id').first()
        
        if latest_bid:
            watchlist_item.latest_bid = latest_bid.bid
        else:
            watchlist_item.latest_bid = "N/A"

    # listings = Listings.objects.all()
    # latest_bid =""
    # listingbids = listings.listing_bids.all()
    # if listingbids:
    #     latest_bid = listingbids.order_by('-bid').first().bid

    return render(request, "auctions/watchlist.html",{
        "watchlist_items": watchlist_items,
       
    })
