from django.contrib import admin
from .models import Genre, Author, Book, Status, Chapter

# Register your models here.
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Status)
admin.site.register(Chapter)