"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from library import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token', TokenObtainPairView.as_view(), name='obtain_token'),
    path('api/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    path('admin/', admin.site.urls),
]
urlpatterns += [
    path('silk/', include('silk.urls', namespace='silk')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

author_router = routers.DefaultRouter()
author_router.register(r'authors', views.AuthorViewSet, basename='authors')
urlpatterns += author_router.urls

genre_router = routers.DefaultRouter()
genre_router.register(r'genres', views.GenresViewSet, basename='genres')
urlpatterns += genre_router.urls

language_router = routers.DefaultRouter()
language_router.register(
    r'languages', views.LanguageViewSet, basename='languages')
urlpatterns += language_router.urls

publisher_router = routers.DefaultRouter()
publisher_router.register(
    r'publishers', views.PublisherViewSet, basename='publishers')
urlpatterns += publisher_router.urls

member_router = routers.DefaultRouter()
member_router.register(
    r'members', views.LibraryMemberViewSet, basename='members')
urlpatterns += member_router.urls

books_router = routers.DefaultRouter()
books_router.register(r'books', views.BookViewSet, basename='books')
urlpatterns += books_router.urls

book_instance_router = routers.DefaultRouter()
book_instance_router.register(
    r'book_instances', views.BookInstanceViewSet, basename='book_instances')
urlpatterns += book_instance_router.urls
