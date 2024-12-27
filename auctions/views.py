from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

from .models import User


def index(request):
    active_listings = Listing.objects.filter(active=True)
    listing_price = []
    for listing in active_listings:
        bids = listing.bids.all()
        if len(bids) == 0:
            listing_price.append(listing.price)
        else:
            listing_price.append(bids.last().price)

    listings_with_prices = zip(active_listings, listing_price)

    return render(request, "auctions/index.html", {
        "active_listings": listings_with_prices,
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

@login_required
def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create_listing.html", {
            "ListingForm": ListingForm
        })
    elif request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            image_url = data.get("image_url")
            if not image_url:
                image_url= "https://static.thenounproject.com/png/4595376-200.png"

            new_listing = Listing(
                owner=request.user,
                title=data.get("title"),
                description=data.get("description"),
                price=float(data.get("price")),
                category=data.get("category"),
                image_url = image_url,
                active=True
            )

            new_listing.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return  HttpResponse("form is not valid")
        
@login_required
def view_listing(request, listing_id):
    # get the message
    message = request.session.pop('message', None)
    
    # find the listing
    listing_list = Listing.objects.filter(id=listing_id)
    if len(listing_list) == 0:
        return HttpResponse("The listing doesn't exist")
    listing = listing_list.last()

    # check if there is winner
    winner_message = None
    if listing.winner and listing.active == False:
        winner = listing.winner
        if request.user == winner:
              winner_message = f"Congratulations! You have won the {listing.title} auction."
        else:
              winner_message = f"Congratulations! {winner} have won the {listing.title} auction."
        
    # checks if the user is the owner
    isMyListing = False
    if (request.user == listing.owner):
        isMyListing = True


    # find the last bid and get the price and user
    # if there is no bid, then bid_price = 0 and winner is None
    bids = listing.bids.all()
    bid_count = bids.count()
    bid_price = 0
    winner = None
    
    if bid_count > 0:
        last_bid = bids.last()
        bid_price = last_bid.price

    # find the comments
    comments = listing.comments.all()

    # check if it is in watch list
    isInWatchList = False
    watch_lists = listing.watch_list.all()
    # check is the user is in listing watch list
    # if so, set isInWatchList = True
    # else set isInWatchList = False
    if request.user in watch_lists:
        isInWatchList = True


 
    return  render(request, "auctions/view_listing.html", {
        "listing": listing,
        "bid_count": bid_count,
        "bid_price": bid_price,
        "CommentForm": CommentForm,
        "BidForm": BidForm,
        "comments": comments,
        "isInWatchList": isInWatchList,
        "isMyListing": isMyListing,
        "message": message,
        "winner_message": winner_message

    })

@login_required
def update_bid(request):
     if request.method == "POST":
        # get the listing id and listing object
        listing_id = int(request.POST.get("listing_id"))
        listing = Listing.objects.get(id=listing_id)

        form = BidForm(request.POST)
        if form.is_valid():
            bid_price = form.cleaned_data.get("price")

        
            #check if there is any bids
            # if there is no bid, the bid must be higher than or equal to the listing price
            previous_bids = listing.bids.all()
            
            # if there is no bid, the bid price must be higher than the listing price
            if len(previous_bids) == 0:
                if bid_price >= listing.price:
                    new_bid = Bid(user=request.user, price=bid_price)
                    new_bid.save()
                    listing.bids.add(new_bid)

                    # if the listing is not in the watch list, add it
                    if request.user not in listing.watch_list.all():
                        listing.watch_list.add(request.user)
                    listing.save()
                else:
                    request.session['message'] = "The bid price must be higher than the listing price"
                    

            # if there are bids, then the bid price must be higher than the last bid
            elif len(previous_bids) > 0:
                previous_bids = listing.bids.all()
                last_bid = previous_bids.last()

                if bid_price > last_bid.price:
                     new_bid = Bid(user=request.user, price=bid_price)
                     new_bid.save()
                     listing.bids.add(new_bid)
                       # if the listing is not in the watch list, add it
                     if request.user not in listing.watch_list.all():
                        listing.watch_list.add(request.user)
                     listing.save()
                else:
                    request.session['message'] = "The bid price must be higher than the last bid price"     

            return HttpResponseRedirect(reverse("view_listing", kwargs={'listing_id': listing_id}))
                
                
        else:
            return HttpResponse("The data is not valid")



@login_required
def close_listing(request):
    if request.method == "POST":
        # get the listing id and listing object
        listing_id = int(request.POST.get("listing_id"))
        listing = Listing.objects.get(id=listing_id)

        # get all the bids
        bids = listing.bids.all()
        bid_count = bids.count()
        bid_price = 0
        winner = None
        
        # if there is no bid, then you can't close the auction
        if bid_count == 0:
            request.session['message'] = "Can't close the listing. There's no bid."
            return HttpResponseRedirect(reverse("view_listing", kwargs={'listing_id': listing_id}))
        
        # if there is bid, close the listing
        # change the listing active status to False
        # get the winner 
        # if request.user == listing.winner 
        if bid_count > 0:
            last_bid = bids.last()
            winner = last_bid.user
            listing.active = False
            listing.winner = winner
            listing.save()


        return HttpResponseRedirect(reverse("view_listing", kwargs={'listing_id': listing_id}))



@login_required    
def add_comment(request):
     if request.method == "POST":
        try:
            listing_id = int(request.POST.get("listing_id"))
            lisiting = Listing.objects.get(id=listing_id)
        except:
            return HttpResponse("The listing doesn't exit anymore")
        
    
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get("text")
            new_comment = Comment(user=request.user, text=text)
            new_comment.save()
            lisiting.comments.add(new_comment)
            lisiting.save()        
            return HttpResponseRedirect(reverse("view_listing", kwargs={'listing_id': listing_id}))
            
        else:
            return HttpResponse("Comment is not valid")
        


def category(request):
    categories = Category.objects.all()
    listings = Listing.objects.filter(active=True)
    selected_category = "all"
    if request.method == "POST":
        categoryData = request.POST.get("category")
        if categoryData == "all":
            return render(request, "auctions/categories.html", {"listings": listings, "categories": categories,"selected_category": selected_category})
        
        wanted_category = Category.objects.get(name=categoryData)
        wanted_listings = Listing.objects.filter(category=wanted_category, active=True)
        return render(request, "auctions/categories.html", {"listings": wanted_listings, "categories": categories, "selected_category": categoryData})      
    else:  
        return render(request, "auctions/categories.html", {"listings": listings, "categories": categories, "selected_category": selected_category})



@login_required
def watch_list(request):
    current_user = request.user
    if request.method == "GET":
        watch_listings = current_user.watch_lists.all()
        print(watch_listings)
       
        return render(request, "auctions/watch_list.html", {
            "watch_listings": watch_listings
        })
    elif request.method == "POST":
        listing_status = request.POST.get("listing_status")
        if listing_status == "all":
            watch_listings = current_user.watch_lists.all()
        elif listing_status == "active":
            watch_listings = current_user.watch_lists.filter(active=True)
        elif listing_status == "closed":
            watch_listings = current_user.watch_lists.filter(active=False)


        return render(request, "auctions/watch_list.html", {
            "watch_listings": watch_listings,
            "listing_status": listing_status
        })
    

@login_required
def add_watch_list(request):
    if request.method == "POST":
        listing_id = int(request.POST["listing_id"])
        listing = Listing.objects.get(id=listing_id)
        listing.watch_list.add(request.user)
        listing.save()
        return HttpResponseRedirect(reverse("view_listing", kwargs={
            'listing_id': listing_id
            }))



@login_required
def remove_watch_list(request):
    if request.method == "POST":
        listing_id = int(request.POST["listing_id"])
        listing = Listing.objects.get(id=listing_id)
        listing.watch_list.remove(request.user)
        listing.save()
        return HttpResponseRedirect(reverse("view_listing", kwargs={
            'listing_id': listing_id
            }))