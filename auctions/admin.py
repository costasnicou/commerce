from django.contrib import admin
from .models import ListingCategories, Listings, ListingComments, ListingBids, WhatchList
# Register your models here.

admin.site.register(Listings)
admin.site.register(ListingCategories)
admin.site.register(ListingComments)
admin.site.register(ListingBids)
admin.site.register(WhatchList)