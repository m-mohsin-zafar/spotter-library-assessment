from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'authors', views.AuthorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/<int:user_id>/favorites', views.favorites_list),
    path('users/<int:user_id>/favorites/add/<int:book_id>/', views.add_to_favorites),
    path('users/<int:user_id>/favorites/remove/<int:book_id>/', views.remove_from_favorites),
]