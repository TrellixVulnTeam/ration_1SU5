from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from core.models import Item, User_Item, Profile, Taglist


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ItemForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Separate tags with ';'"}))

    class Meta:
        model = Item
        fields = ['name', 'tags', 'url', 'description', 'image']


class UserItemForm(forms.ModelForm):
    class Meta:
        model = User_Item
        fields = ['rating', 'interest']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fullname', 'picture', 'bio', 'location', 'website']


class TaglistForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Separate tags with ';'"}))

    class Meta:
        model = Taglist
        fields = ['name', 'tags', 'description', 'is_private', 'is_main']
