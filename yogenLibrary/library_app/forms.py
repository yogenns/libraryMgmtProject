from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Genre, Author


class CreateUserForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1')
        model = get_user_model()

    # Use below to update Labels of fields on Sign Up Page
    # def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['email'].label = 'Email Address'


class CreateGenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'textinputclass'}),
        }


class CreateAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'textinputclass'}),
        }
