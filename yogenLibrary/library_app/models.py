from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Genre(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Book(models.Model):
    book_file = models.FileField(upload_to="library_app/", default='')
    title = models.CharField(max_length=1024)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    book_cover = models.ImageField(upload_to="library_app/")
    description = models.TextField()
    uploader = models.CharField(max_length=1024)
    publication = models.CharField(max_length=1024)
    year = models.IntegerField(
        validators=[MaxValueValidator(3000), MinValueValidator(-3000)])

    def __str__(self):
        return self.title
