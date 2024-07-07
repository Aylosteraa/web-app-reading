from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.creating_book, name='book'),
    path('book/chapter', views.creating_chapter, name='chapter'),
]