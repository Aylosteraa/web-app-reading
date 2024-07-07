from django.shortcuts import render
from .models import Genre, Book, Author, Status, Chapter
from user.models import Review, Comentary, CustomUser, Like
from django.db.models import Max
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib import messages

# Create your views here.
def index(request):
	if request.user.is_authenticated: 
		genres = Genre.objects.all()
		books = Book.objects.all().order_by('-updated_at')[:10]
		popular_books = Book.objects.all().order_by('-views')[:5]
		context = {
			'genres' : genres,
			'books' : books,
			'popular_books' : popular_books
			}
		return render(request, 'main.html', context)
	else:
		return redirect('sign_in')

def search_view(request):
	query = request.GET.get('search', '')
	results = Book.objects.filter(name__icontains=query)	
	return render(request, 'search-page.html', 
			   {'results' : results, 'query':query})

def search_by_genres(request):
	genre_ids = request.GET.getlist('genre')
	books = Book.objects.all()
	genres, books = filter_by_genres(genre_ids, books)
	context = {
		'results':books,
		'genres':genres
	}
	return render(request, 'search-page.html', context)

def book_page(request):
	genre_ids = request.GET.getlist('genre')
	books = Book.objects.all()
	genres, books = filter_by_genres(genre_ids, books)
	context = {
		'results':books,
		'genres':genres
	}
	return render(request, 'search-page.html', context)

def filter_by_genres(genre_ids, books):
	try:
		genres = Genre.objects.filter(id__in=genre_ids)
		print(genres)
		for genre in genres:
			books = books.filter(genres=genre)
	except Genre.DoesNotExist:
		books = []
	return genres, books

def cataloge_view(request):
	books = Book.objects.all()
	genres = Genre.objects.all()
	context = {
		'books' : books,
		'genres' : genres
	}
	
	return render(request, 'cataloge.html', context)

def sort(request):
	books=Book.objects.all()
	if(request.GET.get('status')):
		status = request.GET.get('status')
		books = books.filter(status_id=status)

	if(request.GET.get('sort')):
		sort = request.GET.get('sort')
		if sort == '1':
			books = books.order_by('-average_point')
		elif sort == '2':
			books = books.order_by('-views')

	if(request.GET.getlist('genre')):
		genre_ids = request.GET.getlist('genre')
		genres, books = filter_by_genres(genre_ids, books)

	genres = Genre.objects.all()

	context = {
		'books' : books,
		'genres' : genres
	}
	

	return render(request, 'cataloge.html', context)
@csrf_exempt

def bookpage(request, bookid):
	if request.user.is_authenticated: 
		user = request.user
		books = Book.objects.get(id = bookid)
		authors = books.authors.all()
		genres = books.genres.all()
		status = Status.objects.get(id = books.status_id.id)
		chapters = range(books.chapter_numder)
		reviews = Review.objects.filter(book_id = books.id)
		average = 0
		lenght = 0
		for review in reviews:
			average+=review.rating
			lenght+=1
		if(lenght!=0):
			average= average / lenght
		reviews = reviews.order_by('-likes').first()
		settings = 0
		if(user.username == authors[0].name):
			settings = 1
		context = {
			'books' : books,
			'authors': authors,
			'genres': genres,
			'status': status,
			'chapters': chapters,
			'reviews': reviews,
			'average': average,
			'user': user.username,
			'settings': settings
			}
		return render(request, 'book_page.html', context)
	else: return redirect('sign_in')

def chapter(request, bookid, chapterid):
	if request.user.is_authenticated: 
		user = request.user
		chapters = Chapter.objects.filter(book_id = bookid)
		length = 0
		for chapter in chapters:
			length+=1
		chapters = chapters.get(number = chapterid)
		comentarys = Comentary.objects.filter(book_id = bookid)
		comentarys = comentarys.filter(chapter_number = chapterid)
		context = {
			'chapters': chapters,
			'comentarys': comentarys,
			'length': length,
			}
		return render(request, 'chapter_page.html', context)
	else: return redirect('sign_in')

def review(request, bookid):
	if request.user.is_authenticated: 
		books = Book.objects.get(id = bookid)
		authors = books.authors.all()
		status = Status.objects.get(id = books.status_id.id)
		reviews = Review.objects.filter(book_id = books.id)
		context = {
			'books' : books,
			'authors': authors,
			'status': status,
			'reviews': reviews,
		}
		return render(request, 'review_page.html', context)
	else: return redirect('sign_in')

def comentar(request, bookid, chapterid):
	user = request.user
	userid = CustomUser.objects.get(id=user.id)
	booksid = Book.objects.get(id=bookid)
	chapters = Chapter.objects.filter(book_id = bookid)
	chapters = chapters.get(number = chapterid)
	if request.method == 'POST':
		comm = request.POST.get('commentar')
		commentar = Comentary.objects.create(user_id=userid, book_id=booksid, chapter_number=chapters, textofcomentary=comm, posting_date='2020-05-30-15:59:02')
	return redirect('chapter', bookid = bookid, chapterid = chapterid)

def bookreview(request, bookid):
	user = request.user
	userid = CustomUser.objects.get(id=user.id)
	booksid = Book.objects.get(id=bookid)
	if request.method == 'POST':
		comm = request.POST.get('reviewtext')
		rating = request.POST.get('rating')
		commentar = Review.objects.create(user_id=userid, book_id=booksid, textofreview=comm,likes=0, rating = rating, posting_date='2020-05-30-15:59:02')
	return redirect('review', bookid = bookid)

def likereview(request, bookid, reviewid):
	user = request.user
	userid = CustomUser.objects.get(id=user.id)
	reviews = Review.objects.get(id=reviewid)
	status = Like.objects.filter(user_id = user.id)
	status = Like.objects.filter(review_id = reviewid)
	if not status:
		status = Like.objects.create(user_id = userid, review_id = reviews)
		reviews.likes = reviews.likes + 1
		reviews.save()
	else:
		status.delete()
		reviews.likes = reviews.likes - 1
		reviews.save()
	return redirect('review', bookid = bookid)

def status_book(request, bookid):
	if request.method == 'POST':
		choice = request.POST.get('status')
	return redirect('bookpage', bookid = bookid)

def updatebook(request, bookid):
	genres = Genre.objects.all()
	status = Status.objects.all()
	books = Book.objects.get(id = bookid)
	context = {
            'genres': genres,
            'status': status,
			'number': books.chapter_numder + 1,
			'book': books
        }
	return render(request, 'updating.html', context)

def addchapter(request, bookid, chapterid):
	context = {
		'book': bookid,
		'chapter': chapterid
	}
	return render(request, 'adding_chapter.html', context)

def adding(request, bookid, chapterid):
	if request.user.is_authenticated: 
		user = request.user
		if request.method == 'POST':
			name = request.POST.get('chaptername')
			text = request.POST.get('chaptertext')
			book = Book.objects.get(id = bookid)
			chapter = Chapter.objects.create(name = name, book_id = book, chapter_text = text, number = chapterid)
			book.chapter_numder = book.chapter_numder + 1
			book.save()
		return redirect('bookpage', bookid = book.id)
	
def updating(request, bookid):
	if request.user.is_authenticated: 
		user = request.user
		book = Book.objects.get(id = bookid)
		if request.method == 'POST':
			synopsis = request.POST.get('synopsis')
			bookstatus = request.POST.get('bookstatus')
			name = request.POST.get('name')
			cover = request.POST.get('cover')
			genre = request.POST.get('genres')
			if synopsis:
				book.synopsis = synopsis
			if bookstatus!='Статус':
				book.status_id = Status.objects.get(name = bookstatus)
			if name:
				book.name = name
			if cover:
				book.cover = cover
			if genre!='Жанри':
				book_genre = Genre.objects.get(name = genre)
				book.genres.clear()
				book.genres.add(book_genre)

			book.save()
	return redirect('bookpage', bookid = bookid)

