from django.shortcuts import render
from .models import Message
from books.models import Book
from user.models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def forum(request, bookid):
	if request.user.is_authenticated: 
		user = request.user
		messages = Message.objects.filter(book_id = bookid)
		context = {
			'user': user,
			'messages': messages,
			'bookid': bookid,
		}
	return render(request, 'forum.html', context)

def forumpost(request, bookid):
	if request.user.is_authenticated: 
		user = request.user
		if request.method == 'POST':
			message = request.POST.get('message')
			book = Book.objects.get(id=bookid)
			username = CustomUser.objects.get(id = user.id)
			postedmessage = Message.objects.create(book_id = book, user_id = username, message_text = message, posting_date = '2020-05-30-15:59:02')
	return redirect('forum', bookid=bookid)