from django import forms
from .models import ListingCategories


class BidForm(forms.Form):
    bid = forms.DecimalField(label="Place your Bid")

class CommentsForm(forms.Form):
    comment = forms.CharField(
        label="Add your comment",
        required=True,
        widget=forms.Textarea(attrs={'class':'form-style'})
    )


class AddListingForm(forms.Form):
    # title
    
    title = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Provide a listing title"})
    )
    # description
    description = forms.CharField(   
        required=True,
        widget=forms.Textarea(attrs={'class':'form-style form-control', 'placeholder':"Add a Listing Description" })
    )
    # starting price
    starting_bid = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Your starting Bid'})
    )
    # image url
    image_url = forms.URLField(
        label="Optionally provide an image url",
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control','placeholder':'Optionally provide an image url'})
    )
    # category
    category = forms.ModelChoiceField(
        queryset=ListingCategories.objects.all(),
        required=False,
        empty_label="Optionally provide a category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

