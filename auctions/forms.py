from .models import *
from django.forms import ModelForm, TextInput, NumberInput, URLInput, Select
from django import forms


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "category", "price", "image_url"]

        widgets = {
                'title': TextInput(attrs={
                    'class': "form-control mb-3",
                    'id': "title"
                    }),
                'description': TextInput(attrs={
                    'class': "form-control mb-3", 
                    'id': "description",
                    "maxlength": 1000 
                    }),
                'category': Select(attrs={
                    'class': "form-control mb-3", 
                    'id': "category",
                    }),

                'price': NumberInput(attrs={
                    'class': "form-control mb-3", 
                    'id': "price",
                    }),

                'image_url': URLInput(attrs={
                    'class': "form-control mb-3", 
                    'id': "price",
                    }),

            }
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]

        widgets = {
                'text': TextInput(attrs={
                    'class': "form-contro w-75 ps-3",
                    'id': "title"
                    }),
            }
        

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["price"]

        widgets = {
           'price': NumberInput(attrs={
                    'class': "form-control mb-3", 
                    'id': "price",
                }), 
        }



