from django import forms
from .models import ListingCategories

listing_categories = ListingCategories.objects.all()
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
        widget=forms.TextInput(attrs={'class': 'form-field'})
    )
    # description
    description = forms.CharField(
        label="Add Listing Description",
        required=True,
        widget=forms.Textarea(attrs={'class':'form-style'})
    )
    # starting price
    starting_bid = forms.DecimalField(
        label="Your starting Bid",
        widget=forms.NumberInput(attrs={'class':'form-field'})
    )
    # image url
    imgage_url = forms.URLField(
        label="Optionally provide an image url",
        widget=forms.URLInput(attrs={'class': 'form-field'})
    )
    # category
    category = forms.ModelChoiceField(
        queryset=listing_categories,
        required=True,  
        widget=forms.Select(attrs={'class': 'form-field'})
    )

