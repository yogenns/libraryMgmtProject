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


class UploadBookForm1(forms.Form):
    book_file = forms.FileField(widget=forms.FileInput(
        attrs={'accept': 'application/pdf, application/epub+zip'}))


class SelectAuthorForm2(forms.Form):
    title = forms.CharField(max_length=1024)
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(), widget=forms.Select(attrs={'onchange': "myFunction(this.name);"}), label="Existing Author", required=False)
    author_name = forms.CharField(max_length=100)
    genre = forms.ModelChoiceField(queryset=Genre.objects.all())
    book_cover = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea)
    uploader = forms.CharField(max_length=1024)
    publication = forms.CharField(max_length=1024)
    year = forms.IntegerField()
