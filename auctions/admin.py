from django.contrib import admin
from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "category", "price", "image_url", "active","winner", "date")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "price")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "text")


# class WatchListAdmin(admin.ModelAdmin):
#     list_display = ("id", "user", "listing")



admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
# admin.site.register(WatchList, WatchListAdmin)