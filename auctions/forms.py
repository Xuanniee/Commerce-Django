from django import forms
from .categories import COMMERCE_CATEGORIES
from .models import Comment

# Python Classes for Various Django Forms

# Auction Listing
class NewListing(forms.Form):
    title = forms.CharField(max_length=128, min_length=1, label="Listing Title:"
                            # Django Forms can pass in CSS like this
                            , widget=forms.TextInput(attrs= {'class': 'form-control'}))
    description = forms.CharField(
        label="Description of Item(s):",
        # Making the Inpput Field a Text Area
        widget=forms.Textarea(
            # Setting Size of Textarea
            attrs={ "size": "auto",
                    "class": "form-control",
                    "resize": None}
        )
    )
    starting_bid = forms.DecimalField(max_digits=20, decimal_places=2, label="Starting Bid:", widget=forms.TextInput(attrs= {'class': 'form-control'}))
    category = forms.CharField(label="Category: ", widget=forms.Select(choices=COMMERCE_CATEGORIES, attrs= {'class': 'form-control'}))
    image_url = forms.URLField(empty_value=None, required=False, label="Image URL (if applicable)", widget=forms.TextInput(attrs= {'class': 'form-control'}))

# Form for Comments
class CommentForm(forms.ModelForm):
    comment_area = forms.CharField(label="", \
                                  widget=forms.Textarea(
                                    attrs={
                                        "class": "form-control",
                                        "resize": None,
                                        "size": "auto",
                                        "placeholder": "Write your Comments here!!"
                                    }
                                  ))
    class Meta:
        model = Comment
        # Specifies which Fields we want User to Type in their Inputs
        fields = ['comment_area']