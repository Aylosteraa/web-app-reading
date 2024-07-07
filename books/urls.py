from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=''),
	path('search/', views.search_view, name='search'),
	path('search_genres/', views.search_by_genres, name='search_genres'),
	path('cataloge/', views.cataloge_view, name='cataloge'),
	path('cataloge/sort/', views.sort, name='sort'),
    path('bookpage/<bookid>/', views.bookpage, name='bookpage'),
    path('bookpage/<bookid>/status', views.status_book, name='status'),
    path('bookpage/<bookid>/chapter/<chapterid>', views.chapter, name='chapter'),
    path('bookpage/<bookid>/chapter/<chapterid>/comentar', views.comentar, name='comentar'),
    path('bookpage/<bookid>/review', views.bookreview, name='book_review'),
    path('bookpage/<bookid>/review/<reviewid>', views.likereview, name='like_review'),
    path('bookpage/<bookid>/reviews', views.review, name='review'),
    path('bookpage/<bookid>/update', views.updatebook, name='updatebook'),
    path('bookpage/<bookid>/update/book', views.updating, name='updating'),
    path('bookpage/<bookid>/update/added/<chapterid>', views.adding, name='adding'),
    path('bookpage/<bookid>/update/chapter/<chapterid>', views.addchapter, name='addchapter'),
]