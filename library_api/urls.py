from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.BookList.as_view()),
    path("books/<int:book_id>/", views.BookDetail.as_view()),
    path("authors/", views.AuthorList.as_view()),
    path("authors/<int:author_id>/", views.AuthorDetail.as_view()),
    # path("users/", views.users_List),
    # path("users/<int:user_id>/", views.user_Detail),
    # path("users/<int:user_id>/favorite/", views.user_Favorite),
    # path("users/<int:user_id>/favorite/<int:book_id>/", views.user_Favorite),
]