from django.shortcuts import render

def creating_book(request):
	return render(request, 'creating_book.html')

def creating_chapter(request):
	return render(request, 'creating_chapter.html')
