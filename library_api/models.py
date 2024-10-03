from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

# There are Authors, and they write Books.
# Each Author can write multiple Books.
# Each Book can have multiple Authors.
# A User can mark a Book as favorite.
# One User can mark multiple Books as favorite.
# One Book can be marked as favorite by multiple Users.

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    dob = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    class Meta:
        db_table = 'author'
        indexes = [
            models.Index(fields=['first_name', 'last_name'])
        ]

class Book(models.Model):
    title = models.CharField(max_length=100, null=False, unique=True)
    authors = models.ManyToManyField(Author, related_name='books')
    published_date = models.DateField(null=False)
    isbn = models.CharField(max_length=13, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def clean(self):
        if not self.authors.exists():
            raise ValidationError('A book must have at least one author.')
    
    class Meta:
        db_table = 'book'
        indexes = [
            models.Index(fields=['title', 'published_date'])
        ]

User.add_to_class('favorite_books', models.ManyToManyField(Book, related_name='favorited_by'))