from django import forms

class BidForm(forms.Form):
    bid = forms.DecimalField(label="Place your Bid")

class CommentsForm(forms.Form):
    comment = forms.CharField(
        label="Add your comment",
        required=True,
        widget=forms.Textarea(attrs={'class':'form-style'})
    )
# class CloseListing(forms.Form):
#     comment = forms.CharField(
#         label="Add your comment",
#         required=True,
#         widget=forms.Textarea(attrs={'class':'form-style'})
#     )