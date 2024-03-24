from django import forms

class UserInputData(forms.Form):
    genre_data = forms.CharField(required=False, widget=forms.HiddenInput())
    username_data = forms.CharField(max_length=100)