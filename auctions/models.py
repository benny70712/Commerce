from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"
    

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    price = models.DecimalField(max_digits=11, decimal_places=2, null=True)

    def __str__(self):
        return f"User:{self.user} Bid:{self.price}"

class Comment(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
        text = models.CharField(max_length=1000)
        
        def __str__(self):
             return f"User: {self.user} Comment: {self.text}"
        


# class Winner(models.Model):
#      user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner")
#      message = models.CharField(max_length=1000)

#      def __str__(self):
#           return f"Winner: {self.user} Message: {self.message}"
     

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", null=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listing")
    price = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    image_url = models.URLField(null=True, blank=True)
    active = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True, null=True)
    bids = models.ManyToManyField(Bid, blank=True, related_name="listings")
    comments = models.ManyToManyField(Comment, related_name="listings", blank=True)
    watch_list = models.ManyToManyField(User, related_name="watch_lists", blank=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won_listings", null=True, blank=True)

    def __str__(self):
        return f"{self.owner} {self.title} {self.price} {self.category}"







