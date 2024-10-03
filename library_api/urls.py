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
]

# urlpatterns = [

#     # path("users/", views.users_List),
#     # path("users/<int:user_id>/", views.user_Detail),
#     # path("users/<int:user_id>/favorite/", views.user_Favorite),
#     # path("users/<int:user_id>/favorite/<int:book_id>/", views.user_Favorite),
# ]