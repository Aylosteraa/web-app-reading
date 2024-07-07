from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, UserLibrary, Review
from forum.models import Message
from books.models import Book, Genre, Author, Status, Chapter
from django.contrib.auth import authenticate, login, logout
import json
import datetime
from datetime import datetime
from books.views import bookpage


@csrf_exempt
def sign_up_post(request):
    if request.method == 'POST':
        try:
            data = request.POST
            print(data)
            first_name = data.get('first_name')
            last_name = data.get('second_name')
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            # Перевірка, чи користувач з таким ім'ям вже існує
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Користувач з таким ім\'ям вже існує'})

            # Створення нового користувача
            user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password, email=email)
            return redirect('sign_in')
        except Exception as e:
            return JsonResponse({'error': f'Помилка: {str(e)}'})

    return JsonResponse({'error': 'Метод не підтримується'})

def sign_in_post(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Аутентифікація користувача за допомогою електронної пошти та пароля
        user = authenticate(request, username=username, password=password)
        print(user)

        if user is not None:
            # Авторизація користувача
            login(request, user)
            return redirect('')
        else:
            # Користувач не знайдений або неправильний пароль
            return render(request, 'sign_in.html', {'error_message': 'Неправильна електронна пошта або пароль'})
    else:
        return render(request, 'sign_in.html')
        

def logout_view(request):
    if request.user.is_authenticated: 
        logout(request)
    return redirect('sign_in')

# Create your views here.
def index(request):
    # чи є користувач авторизованим
    if request.user.is_authenticated: 
        user = request.user
        user_id = user.id
        user_books = UserLibrary.objects.filter(user_id=user_id)
        finished = user_books.filter(choices='F').values_list("book_id")
        in_process = user_books.filter(choices='IP').values_list("book_id")
        give_over = user_books.filter(choices='GO').values_list("book_id")
        planned = user_books.filter(choices='P').values_list("book_id")
        created = user_books.filter(choices='C').values_list("book_id")

        finished_books = Book.objects.filter(id__in = finished)
        in_process_books = Book.objects.filter(id__in = in_process)
        give_over_books = Book.objects.filter(id__in = give_over)
        planned_books = Book.objects.filter(id__in = planned)
        created_books = Book.objects.filter(id__in = created)

        reviews = Review.objects.filter(user_id = user_id)
        forums_ids = Message.objects.filter(user_id = user_id).values('book_id').distinct()
        books_ids = list()
        for forum in forums_ids:
            books_ids.append(forum['book_id'])
        forums = Book.objects.filter(id__in=books_ids)
        context = {
            'user':user,
            'finished_books':finished_books,
            'in_process_books':in_process_books,
            'give_over_books':give_over_books,
            'planned_books':planned_books,
            'created_books':created_books,
            "reviews": reviews,
            "forums": forums
        }
        return render(request, 'user.html', context)
    else:
        return redirect('sign_in')
    
def delete_planned_book(request):
    if request.user.is_authenticated: 
        user = request.user
        user_id = user.id
        if request.method == 'POST':
            book_id = request.POST['book_id']
            book = get_object_or_404(UserLibrary, book_id=book_id, user_id=user_id)
            book.delete()
    return redirect('')

def sign_in(request):
	return render(request, 'sign_in.html')

def sign_up(request):
	return render(request, 'sign_up.html')

def user_update(request):
    if request.user.is_authenticated: 
        user = request.user
    return render(request, 'user_update.html', {'user': user})

def update(request):
    if request.user.is_authenticated: 
        user = request.user
        if request.method == 'POST':
            if request.POST['first_name']:
                user.first_name = request.POST['first_name']
            if request.POST['last_name']:
                user.last_name = request.POST['last_name']
            if request.POST['username']:
                user.username = request.POST['username']
            if request.POST['email']:
                user.email = request.POST['email']
            if request.POST['password']:
                user.password = request.POST['password']
            if request.FILES.get('avatar'):
                user.avatar = request.FILES['avatar']
                print(user.avatar.url)
            user.save()
        return redirect('')
    else: 
        return redirect('sign_in')

def create_book(request):
    genres = Genre.objects.all()
    status = Status.objects.all()
    context = {
            'genres': genres,
            'status': status,
        }
    return render(request, 'creating_book.html', context)

def createbook(request):
    if request.user.is_authenticated: 
        user = request.user
        genres = Genre.objects.all()
        if request.method == 'POST':
            synopsis = request.POST.get('synopsis')
            bookstatus = request.POST.get('bookstatus')
            name = request.POST.get('name')
            author = request.POST.get('author')
            translator = request.POST.get('translator')
            cover = request.POST.get('cover')
            genre = request.POST.get('genres')
            book_genre = Genre.objects.get(name = genre)
            status = Status.objects.get(name = bookstatus)
            if not author:
                author1 = Author.objects.filter(name = user.username)
                if not author1:
                    author = Author.objects.create(name = user.username)
                    book = Book.objects.create(name = name, year = datetime.now().year, average_point = 5, chapter_numder = 0, synopsis = synopsis, cover = cover, translator = translator, status_id = status, views = 0, created_at ='2020-05-30-15:59:02', updated_at = '2020-05-30-15:59:02')
                    book.authors.add(author)
                else:
                    author1 = Author.objects.get(name = user.username)
                    book = Book.objects.create(name = name, year = datetime.now().year, average_point = 5, chapter_numder = 0, synopsis = synopsis, cover = cover, translator = translator, status_id = status, views = 0, created_at ='2020-05-30-15:59:02', updated_at = '2020-05-30-15:59:02')
                    book.authors.add(author1)
                book.genres.add(book_genre)
            else:
                author1 = Author.objects.filter(name = author)
                if not author1:
                    author2 = Author.objects.create(name = author)
                    book = Book.objects.create(name = name, year = datetime.now().year, average_point = 5, chapter_numder = 0, synopsis = synopsis, cover = cover, translator = translator, status_id = status, views = 0, created_at ='2020-05-30-15:59:02', updated_at = '2020-05-30-15:59:02')
                    book.authors.add(author2)
                else:
                    author1 = Author.objects.get(name = author)
                    book = Book.objects.create(name = name, year = datetime.now().year, average_point = 5, chapter_numder = 0, synopsis = synopsis, cover = cover, translator = translator, status_id = status, views = 0, created_at ='2020-05-30-15:59:02', updated_at = '2020-05-30-15:59:02')
                    book.authors.add(author1)
                book.genres.add(book_genre)
            context = {
            'genres': genres,
            'synopsis': synopsis,
            'bookstatus': bookstatus,
            'name': name,
            'author': author,
            'translator': translator,
            'cover': cover,
            'genre': genre,
            'book': book,
            }
        return render(request, 'creating_chapter.html', context)
    else: 
        return redirect('sign_in')
    
def create_chapter(request, bookid):
    if request.user.is_authenticated: 
        user = request.user
        if request.method == 'POST':
            name = request.POST.get('chaptername')
            text = request.POST.get('chaptertext')
            book = Book.objects.get(id = bookid)
            chapter = Chapter.objects.create(name = name, book_id = book, chapter_text = text, number = 1)
            book.chapter_numder = book.chapter_numder + 1
            book.save()
    return redirect('bookpage', bookid = book.id)