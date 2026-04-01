from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    pass


class ListingCategories(models.Model):
    name = models.CharField(max_length=30,blank=False)
    imgurl = models.URLField(max_length=500,blank=True)

    def __str__(self):
        return f"{self.name}"


class Listings(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_listings"
    )
    title = models.CharField(max_length=200,blank=False) 
    description = models.TextField(blank=False)
    starting_price = models.DecimalField(max_digits=10,decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    imgurl = models.URLField(max_length=500,blank=True)
    winner = models.CharField(max_length=200,blank=True)
    category = models.ForeignKey(
        ListingCategories,
        on_delete=models.CASCADE,
        related_name="category_listings",
        blank=True,
        null=True,
    ) 


    class StatusChoices(models.TextChoices):
        ACTIVE = 'T', ('Active')
        INACTIVE ='F', ('Inactive')

    status = models.CharField(
        max_length=1,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
    )

    def __str__(self):
        return f"Title: {self.title}"


class ListingBids(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
       
    )

    listing = models.ForeignKey(
        Listings,
        on_delete=models.CASCADE,
        related_name="listing_bids"
    )

    bid = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"Bid: {self.id} by {self.user.username} on listing {self.listing.title}"

class ListingComments(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        
    )

    listing = models.ForeignKey(
        Listings,
        on_delete=models.CASCADE,
        related_name="listing_comments"
    )

    content = models.TextField(blank=False)

    def __str__(self):
        return f"Comment: {self.id} by {self.user.username} on listing {self.listing.title}"


class WhatchList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
       
    )
    listing = models.ForeignKey(
        Listings,
        on_delete=models.CASCADE,
        related_name="user_watchlist"
    )


    def __str__(self):
            return f"{self.user} by {self.listing.title}"
