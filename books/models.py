from django.db import models
# Create your models here.
class Genre(models.Model):
	id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	name = models.CharField(max_length=50)

class Author(models.Model):
	id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	name = models.CharField(max_length=150)

class Status(models.Model):
	id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	name = models.CharField(max_length=150)

class Book(models.Model):
	id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	name = models.CharField(max_length=150)
	year = models.PositiveIntegerField()
	average_point = models.FloatField()
	chapter_numder = models.IntegerField()
	synopsis = models.TextField()
	cover = models.ImageField(upload_to='static/img/books/') #pip install Pilow
	authors = models.ManyToManyField(Author, blank=True)
	translator = models.CharField(max_length=150, null=True)
	genres = models.ManyToManyField(Genre, blank=True)
	status_id = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
	views = models.IntegerField(null=True)
	created_at = models.DateTimeField(null=True)
	updated_at = models.DateTimeField(null=True)

class Chapter(models.Model):
	id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	name = models.CharField(max_length=150, null=True)
	book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
	chapter_text = models.TextField()
	number = models.PositiveIntegerField()




