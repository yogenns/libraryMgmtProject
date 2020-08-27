from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Genre, Author, RecommendedBook, Book


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
    genre = forms.ModelChoiceField(queryset=Genre.objects.all())

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


class CreateRecommendedBookForm(forms.ModelForm):

    class Meta:
        model = RecommendedBook
        fields = ('book', 'book_index')

        # FIX THIS LATER.. Need a method call instead of repeating logic
        num_of_recommendations = 8
        choices_list = []
        print("Get Remaining Index")
        for var in range(1, num_of_recommendations+1):
            try:
                RecommendedBook.objects.get(book_index=var)
            except RecommendedBook.DoesNotExist:
                choices_list.append((var, var))
        print(choices_list)
        CHOICES = tuple(choices_list)
        widgets = {
            'book_index': forms.Select(choices=CHOICES),
        }

    def get_choices_for_index(self):
        num_of_recommendations = 8
        choices_list = []
        print("get_choices_for_index")
        for var in range(1, num_of_recommendations+1):
            try:
                RecommendedBook.objects.get(book_index=var)
            except RecommendedBook.DoesNotExist:
                choices_list.append((var, var))
        print(choices_list)
        return tuple(choices_list)

    def __init__(self, *args, **kwargs):
        print("__init__")
        super(CreateRecommendedBookForm, self).__init__(*args, **kwargs)
        self.fields['book_index'].widget.choices = self.get_choices_for_index()
        books = Book.objects.exclude(
            id__in=RecommendedBook.objects.values_list('book', flat=True).all())
        self.fields['book'].queryset = books

    def get_initial(self):
        initial = super().get_initial()
        return initial
