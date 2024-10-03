from django.core.management.base import BaseCommand
from library_api.models import Author, Book
from django.contrib.auth.models import User
from datetime import date
import random

class Command(BaseCommand):
    help = 'Seed database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Clear existing data
        Author.objects.all().delete()
        Book.objects.all().delete()
        User.objects.filter(username='testuser').delete()

        # Create authors
        authors = [
            Author(first_name="John", last_name="Doe", dob=date(1970, 5, 21)),
            Author(first_name="Jane", last_name="Smith", dob=date(1985, 8, 14)),
            Author(first_name="Emily", last_name="Johnson", dob=date(1992, 12, 5)),
        ]
        Author.objects.bulk_create(authors)

        # Create books and assign authors
        books = [
            Book(title="Django for Beginners", published_date=date(2020, 1, 15), isbn="1234567890123"),
            Book(title="Advanced Django Techniques", published_date=date(2021, 6, 10), isbn="1234567890124"),
            Book(title="Python and Django", published_date=date(2019, 3, 22), isbn="1234567890125"),
        ]
        Book.objects.bulk_create(books)

        for book in books:
            book.authors.set(random.sample(authors, k=random.randint(1, len(authors))))
            book.save()

        # Create a test user and mark some books as favorites
        user = User.objects.create_user(username='testuser', password='testpass')
        user.favorite_books.set(random.sample(books, k=random.randint(1, len(books))))
        user.save()

        self.stdout.write(self.style.SUCCESS('Data seeded successfully!'))