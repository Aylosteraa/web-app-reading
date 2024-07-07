from books.models import Book
from user.models import CustomUser
from chat.models import Chat
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def chat(request):
	user = request.user
	chats = Chat.objects.all()
	context ={
		'user': user,
		'chats':chats
    }
	return render(request, 'chat.html', context)