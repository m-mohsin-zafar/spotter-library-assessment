from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class BookList(APIView):
    def get(self, request):
        books = get_list_or_404(Book)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        author_ids = data.pop('authors', [])
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            book = serializer.save()
            authors = Author.objects.filter(pk__in=author_ids)
            book.authors.set(authors)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BookDetail(APIView):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    def put(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        data = request.data
        author_ids = data.pop('authors', [])
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            book = serializer.save()
            authors = Author.objects.filter(pk__in=author_ids)
            book.authors.set(authors)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class AuthorList(APIView):
    def get(self, request):
        authors = get_list_or_404(Author)
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            author = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AuthorDetail(APIView):
    def get(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)
    
    def put(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            author = serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        if author.books.exists():
            return Response({'error': 'Cannot delete an author with associated books.'}, status=status.HTTP_400_BAD_REQUEST)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    