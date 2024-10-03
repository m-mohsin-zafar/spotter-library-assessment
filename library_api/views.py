from django.shortcuts import get_object_or_404, get_list_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, UserSerializer


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['first_name', 'last_name', 'dob']
    
    def destroy(self, request, *args, **kwargs):
        if Author.objects.filter(pk=kwargs['id']).books.exists():
            return Response({'error': 'Cannot delete an author with associated books.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)
    
    
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'authors__first_name', 'authors__last_name', 'isbn']
    ordering_fields = ['title', 'published_date']
    
    def get_queryset(self):
        queryset = Book.objects.all()
        author_id = self.request.query_params.get('author_id')
        if author_id:
            queryset = queryset.filter(authors__id=author_id)
        return queryset
    
    def create(self, request):
        data = request.data
        author_ids = data.pop('authors', [])
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            book = serializer.save()
            authors = Author.objects.filter(pk__in=author_ids)
            book.authors.set(authors)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, id):
        book = get_object_or_404(Book, pk=id)
        data = request.data
        author_ids = data.pop('authors', [])
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            book = serializer.save()
            authors = Author.objects.filter(pk__in=author_ids)
            book.authors.set(authors)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create Two Views 1. Add a Book to user's favorite list 2. Remove a Book from user's favorite list
# User.add_to_class('favorite_books', models.ManyToManyField(Book, related_name='favorited_by'))

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_favorites(request, user_id, book_id):
    if request.user.id != user_id:
        return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        user = User.objects.get(pk=user_id)
        book = Book.objects.get(pk=book_id)
    except (User.DoesNotExist, Book.DoesNotExist):
        return Response({'error': 'User or book not found.'}, status=status.HTTP_404_NOT_FOUND)

    if user.favorite_books.count() >= 20:
        return Response({'error': 'You can only have up to 20 favorite books.'}, status=status.HTTP_400_BAD_REQUEST)

    user.favorite_books.add(book)
    return Response({'message': 'Book added to favorites.'}, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def remove_from_favorites(request, user_id, book_id):
    if request.user.id != user_id:
        return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        user = User.objects.get(pk=user_id)
        book = Book.objects.get(pk=book_id)
    except (User.DoesNotExist, Book.DoesNotExist):
        return Response({'error': 'User or book not found.'}, status=status.HTTP_404_NOT_FOUND)

    user.favorite_books.remove(book)
    return Response({'message': 'Book removed from favorites.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def favorites_list(request, user_id):
    # Ensure the request is made by the user or an admin
    if request.user.id != user_id and not request.user.is_staff:
        return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    favorite_books = user.favorite_books.all()
    serializer = BookSerializer(favorite_books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)